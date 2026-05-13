from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.estoque.models import CategoriaProduto, MovimentacaoEstoque, Produto, UnidadeMedida
from apps.estoque.services import EstoqueService


@pytest.fixture
def produto(db):
    categoria = CategoriaProduto.objects.create(nome="Materia prima")
    unidade = UnidadeMedida.objects.create(sigla="UN", nome="Unidade")
    return Produto.objects.create(
        codigo_interno="PRD-001",
        sku="SKU-001",
        nome="Chapa de aco",
        categoria=categoria,
        unidade_medida=unidade,
        estoque_minimo=Decimal("2.0000"),
    )


@pytest.mark.django_db
def test_registrar_entrada_soma_saldo(produto):
    movimentacao = EstoqueService().registrar_entrada(produto_id=produto.id, quantidade=Decimal("10.0000"))
    produto.refresh_from_db()

    assert produto.estoque_atual == Decimal("10.0000")
    assert movimentacao.tipo == MovimentacaoEstoque.Tipo.ENTRADA
    assert movimentacao.saldo_anterior == Decimal("0.0000")
    assert movimentacao.saldo_posterior == Decimal("10.0000")


@pytest.mark.django_db
def test_registrar_saida_nao_permite_saldo_negativo(produto):
    with pytest.raises(ValidationError):
        EstoqueService().registrar_saida(produto_id=produto.id, quantidade=Decimal("1.0000"))


@pytest.mark.django_db
def test_registrar_saida_baixa_saldo(produto):
    service = EstoqueService()
    service.registrar_entrada(produto_id=produto.id, quantidade=Decimal("8.0000"))
    movimentacao = service.registrar_saida(produto_id=produto.id, quantidade=Decimal("3.0000"))
    produto.refresh_from_db()

    assert produto.estoque_atual == Decimal("5.0000")
    assert movimentacao.tipo == MovimentacaoEstoque.Tipo.SAIDA
    assert movimentacao.saldo_anterior == Decimal("8.0000")
    assert movimentacao.saldo_posterior == Decimal("5.0000")


@pytest.mark.django_db
def test_registrar_ajuste_define_saldo_e_mantem_historico(produto):
    service = EstoqueService()
    service.registrar_entrada(produto_id=produto.id, quantidade=Decimal("8.0000"))
    movimentacao = service.registrar_ajuste(produto_id=produto.id, quantidade=Decimal("4.0000"))
    produto.refresh_from_db()

    assert produto.estoque_atual == Decimal("4.0000")
    assert movimentacao.saldo_anterior == Decimal("8.0000")
    assert movimentacao.saldo_posterior == Decimal("4.0000")
    assert MovimentacaoEstoque.objects.filter(produto=produto).count() == 2
