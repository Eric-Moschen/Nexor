from datetime import date
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.clientes.models import Cliente
from apps.estoque.models import CategoriaProduto, Produto, UnidadeMedida
from apps.orcamentos.enums import StatusOrcamento
from apps.orcamentos.models import HistoricoOrcamento, Orcamento
from apps.orcamentos.services import OrcamentoService


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="comercial", password="test12345", role=User.Role.COMERCIAL)


@pytest.fixture
def cliente(db):
    return Cliente.objects.create(razao_social="Cliente Orcamento", documento="12345678000195")


@pytest.fixture
def produto(db):
    categoria = CategoriaProduto.objects.create(nome="Produtos Orcamento")
    unidade = UnidadeMedida.objects.create(sigla="UNORC", nome="Unidade Orcamento")
    return Produto.objects.create(
        codigo_interno="ORC-PRD-001",
        sku="ORC-SKU-001",
        nome="Produto para proposta",
        categoria=categoria,
        unidade_medida=unidade,
        custo_medio=Decimal("20.0000"),
        preco_venda=Decimal("50.00"),
        estoque_atual=Decimal("3.0000"),
    )


def criar_orcamento(usuario, cliente, produto, **extra):
    dados = {
        "cliente": cliente,
        "titulo": "Proposta comercial",
        "descricao": "Proposta de produto e servico",
        "data_validade": date(2026, 6, 30),
        "valor_desconto": Decimal("5.00"),
    }
    dados.update(extra)
    return OrcamentoService().criar_orcamento(
        usuario=usuario,
        itens_produto=[{"produto": produto, "quantidade": Decimal("2.0000"), "valor_unitario": Decimal("50.00"), "desconto": Decimal("5.00")}],
        itens_servico=[{"descricao": "Instalacao", "quantidade": Decimal("1.0000"), "custo_estimado": Decimal("40.00"), "valor_unitario": Decimal("100.00")}],
        **dados,
    )


@pytest.mark.django_db
def test_criar_orcamento_valido_calcula_totais(usuario, cliente, produto):
    orcamento = criar_orcamento(usuario, cliente, produto)

    assert orcamento.valor_produtos == Decimal("95.00")
    assert orcamento.valor_servicos == Decimal("100.00")
    assert orcamento.valor_total == Decimal("190.00")
    assert orcamento.custo_total == Decimal("80.00")
    assert orcamento.margem_estimada == Decimal("57.89")


@pytest.mark.django_db
def test_bloquear_orcamento_sem_cliente(usuario, produto):
    with pytest.raises(ValidationError):
        OrcamentoService().criar_orcamento(
            usuario=usuario,
            cliente=None,
            titulo="Sem cliente",
            data_validade=date(2026, 6, 30),
            itens_produto=[{"produto": produto, "quantidade": Decimal("1.0000"), "valor_unitario": Decimal("10.00")}],
        )


@pytest.mark.django_db
def test_bloquear_orcamento_sem_itens(usuario, cliente):
    with pytest.raises(ValidationError):
        OrcamentoService().criar_orcamento(usuario=usuario, cliente=cliente, titulo="Sem item", data_validade=date(2026, 6, 30))


@pytest.mark.django_db
def test_aprovar_reprovar_cancelar(usuario, cliente, produto):
    service = OrcamentoService()
    aprovado = criar_orcamento(usuario, cliente, produto)
    service.enviar(orcamento_id=aprovado.id, usuario=usuario)
    aprovado = service.aprovar(orcamento_id=aprovado.id, usuario=usuario)
    assert aprovado.status == StatusOrcamento.APROVADO

    reprovado = criar_orcamento(usuario, cliente, produto, titulo="Outra proposta")
    service.enviar(orcamento_id=reprovado.id, usuario=usuario)
    reprovado = service.reprovar(orcamento_id=reprovado.id, usuario=usuario, motivo="Preco acima do esperado")
    assert reprovado.status == StatusOrcamento.REPROVADO

    cancelado = criar_orcamento(usuario, cliente, produto, titulo="Proposta cancelada")
    cancelado = service.cancelar(orcamento_id=cancelado.id, usuario=usuario)
    assert cancelado.status == StatusOrcamento.CANCELADO


@pytest.mark.django_db
def test_bloquear_reprovacao_sem_motivo(usuario, cliente, produto):
    orcamento = criar_orcamento(usuario, cliente, produto)

    with pytest.raises(ValidationError):
        OrcamentoService().reprovar(orcamento_id=orcamento.id, usuario=usuario, motivo="")


@pytest.mark.django_db
def test_bloquear_edicao_apos_aprovacao(usuario, cliente, produto):
    service = OrcamentoService()
    orcamento = criar_orcamento(usuario, cliente, produto)
    service.enviar(orcamento_id=orcamento.id, usuario=usuario)
    service.aprovar(orcamento_id=orcamento.id, usuario=usuario)

    with pytest.raises(ValidationError):
        service.atualizar_orcamento(orcamento_id=orcamento.id, usuario=usuario, titulo="Novo titulo")


@pytest.mark.django_db
def test_converter_orcamento_aprovado_em_os_e_bloquear_duplicidade(usuario, cliente, produto):
    service = OrcamentoService()
    orcamento = criar_orcamento(usuario, cliente, produto)
    service.enviar(orcamento_id=orcamento.id, usuario=usuario)
    service.aprovar(orcamento_id=orcamento.id, usuario=usuario)
    convertido = service.converter_em_os(orcamento_id=orcamento.id, usuario=usuario)

    assert convertido.status == StatusOrcamento.CONVERTIDO_OS
    assert convertido.ordem_servico is not None
    with pytest.raises(ValidationError):
        service.converter_em_os(orcamento_id=orcamento.id, usuario=usuario)


@pytest.mark.django_db
def test_gerar_pdf_registra_historico(usuario, cliente, produto):
    orcamento = criar_orcamento(usuario, cliente, produto)
    arquivo = OrcamentoService().gerar_pdf(orcamento_id=orcamento.id, usuario=usuario)

    assert arquivo.name.endswith(".pdf")
    assert HistoricoOrcamento.objects.filter(orcamento=orcamento, tipo_evento="pdf").exists()
