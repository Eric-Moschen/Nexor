from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.clientes.models import Cliente
from apps.financeiro.enums import StatusContaPagar, StatusContaReceber, TipoFinanceiro
from apps.financeiro.models import CategoriaFinanceira, CentroCusto
from apps.financeiro.services import FinanceiroService
from apps.fornecedores.models import Fornecedor


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="financeiro", password="test12345", role=User.Role.FINANCEIRO)


@pytest.fixture
def centro(db):
    return CentroCusto.objects.create(codigo="ADM", nome="Administrativo")


@pytest.fixture
def categoria_despesa(db):
    return CategoriaFinanceira.objects.create(nome="Materia prima", tipo=TipoFinanceiro.DESPESA)


@pytest.fixture
def categoria_receita(db):
    return CategoriaFinanceira.objects.create(nome="Vendas", tipo=TipoFinanceiro.RECEITA)


@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(razao_social="Fornecedor Financeiro", documento="11111111000111")


@pytest.fixture
def cliente(db):
    return Cliente.objects.create(razao_social="Cliente Financeiro", documento="22222222000122")


@pytest.mark.django_db
def test_criar_conta_pagar_valida(usuario, centro, categoria_despesa, fornecedor):
    conta = FinanceiroService().criar_conta_pagar(
        usuario=usuario,
        fornecedor=fornecedor,
        descricao="Compra de insumos",
        categoria=categoria_despesa,
        centro_custo=centro,
        valor_original=Decimal("100.00"),
        data_emissao=date(2026, 5, 1),
        data_vencimento=date(2026, 5, 30),
    )

    assert conta.valor_atual == Decimal("100.00")
    assert conta.status == StatusContaPagar.PENDENTE


@pytest.mark.django_db
def test_baixa_parcial_e_total_conta_pagar(usuario, centro, categoria_despesa, fornecedor):
    service = FinanceiroService()
    conta = service.criar_conta_pagar(
        usuario=usuario,
        fornecedor=fornecedor,
        descricao="Compra",
        categoria=categoria_despesa,
        centro_custo=centro,
        valor_original=Decimal("100.00"),
        data_emissao=date(2026, 5, 1),
        data_vencimento=date(2026, 5, 30),
    )

    service.baixar_conta_pagar(conta_id=conta.id, usuario=usuario, valor_pago=Decimal("40.00"), data_pagamento=date(2026, 5, 10))
    conta.refresh_from_db()
    assert conta.valor_atual == Decimal("60.00")
    assert conta.status == StatusContaPagar.PARCIAL

    service.baixar_conta_pagar(conta_id=conta.id, usuario=usuario, valor_pago=Decimal("60.00"), data_pagamento=date(2026, 5, 11))
    conta.refresh_from_db()
    assert conta.valor_atual == Decimal("0.00")
    assert conta.status == StatusContaPagar.PAGO


@pytest.mark.django_db
def test_bloquear_baixa_maior_que_saldo(usuario, centro, categoria_receita, cliente):
    service = FinanceiroService()
    conta = service.criar_conta_receber(
        usuario=usuario,
        cliente=cliente,
        descricao="Venda",
        categoria=categoria_receita,
        centro_custo=centro,
        valor_original=Decimal("50.00"),
        data_emissao=date(2026, 5, 1),
        data_vencimento=date(2026, 5, 30),
    )

    with pytest.raises(ValidationError):
        service.baixar_conta_receber(conta_id=conta.id, usuario=usuario, valor_pago=Decimal("60.00"), data_pagamento=date(2026, 5, 10))


@pytest.mark.django_db
def test_parcelamento_gera_vencimentos(usuario):
    parcelamento, valor, vencimentos = FinanceiroService().gerar_parcelamento(
        descricao="Contrato anual",
        valor_total=Decimal("1200.00"),
        quantidade_parcelas=12,
        data_primeiro_vencimento=date(2026, 1, 31),
        usuario=usuario,
    )

    assert parcelamento.quantidade_parcelas == 12
    assert valor == Decimal("100.00")
    assert len(vencimentos) == 12
