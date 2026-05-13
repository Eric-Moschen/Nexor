from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.compras.models import PedidoCompra, SolicitacaoCompra
from apps.compras.services import ComprasService
from apps.estoque.models import CategoriaProduto, Produto, UnidadeMedida
from apps.fornecedores.models import Fornecedor


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="compras", password="test12345", role=User.Role.COMPRAS)


@pytest.fixture
def supervisor(db):
    return User.objects.create_user(username="supervisor", password="test12345", role=User.Role.SUPERVISOR)


@pytest.fixture
def produto(db):
    categoria = CategoriaProduto.objects.create(nome="Insumos")
    unidade = UnidadeMedida.objects.create(sigla="UN", nome="Unidade")
    produto = Produto.objects.create(
        codigo_interno="INS-001",
        sku="INS-SKU-001",
        nome="Disco de corte",
        categoria=categoria,
        unidade_medida=unidade,
    )
    return produto


@pytest.fixture
def fornecedor(db):
    return Fornecedor.objects.create(razao_social="Fornecedor Teste LTDA", documento="12345678000190")


def item_payload(produto):
    return {
        "produto": produto,
        "descricao_livre": "",
        "quantidade_solicitada": Decimal("5.0000"),
        "unidade_medida": produto.unidade_medida,
        "observacao": "",
    }


@pytest.mark.django_db
def test_criar_solicitacao_valida(usuario, produto):
    solicitacao = ComprasService().criar_solicitacao(
        solicitante=usuario,
        centro_custo="Producao",
        justificativa="Reposicao de insumos",
        prioridade=SolicitacaoCompra.Prioridade.MEDIA,
        itens=[item_payload(produto)],
    )

    assert solicitacao.status == SolicitacaoCompra.Status.RASCUNHO
    assert solicitacao.itens.count() == 1


@pytest.mark.django_db
def test_bloquear_solicitacao_sem_itens(usuario):
    with pytest.raises(ValidationError):
        ComprasService().criar_solicitacao(
            solicitante=usuario,
            centro_custo="Producao",
            justificativa="Sem itens",
            prioridade=SolicitacaoCompra.Prioridade.MEDIA,
            itens=[],
        )


@pytest.mark.django_db
def test_fluxo_aprovacao(usuario, supervisor, produto):
    service = ComprasService()
    solicitacao = service.criar_solicitacao(
        solicitante=usuario,
        centro_custo="Manutencao",
        justificativa="Compra emergencial",
        prioridade=SolicitacaoCompra.Prioridade.ALTA,
        itens=[item_payload(produto)],
    )

    service.enviar_para_aprovacao(solicitacao_id=solicitacao.id, usuario=usuario)
    solicitacao = service.aprovar_solicitacao(solicitacao_id=solicitacao.id, usuario=supervisor)

    assert solicitacao.status == SolicitacaoCompra.Status.APROVADA
    assert solicitacao.aprovador == supervisor


@pytest.mark.django_db
def test_reprovar_exige_motivo(usuario, supervisor, produto):
    service = ComprasService()
    solicitacao = service.criar_solicitacao(
        solicitante=usuario,
        centro_custo="Manutencao",
        justificativa="Compra",
        prioridade=SolicitacaoCompra.Prioridade.MEDIA,
        itens=[item_payload(produto)],
    )
    service.enviar_para_aprovacao(solicitacao_id=solicitacao.id, usuario=usuario)

    with pytest.raises(ValidationError):
        service.reprovar_solicitacao(solicitacao_id=solicitacao.id, usuario=supervisor, motivo="")


@pytest.mark.django_db
def test_converter_solicitacao_aprovada_em_pedido(usuario, supervisor, produto, fornecedor):
    service = ComprasService()
    solicitacao = service.criar_solicitacao(
        solicitante=usuario,
        centro_custo="Producao",
        justificativa="Reposicao",
        prioridade=SolicitacaoCompra.Prioridade.MEDIA,
        itens=[item_payload(produto)],
    )
    service.enviar_para_aprovacao(solicitacao_id=solicitacao.id, usuario=usuario)
    service.aprovar_solicitacao(solicitacao_id=solicitacao.id, usuario=supervisor)

    pedido = service.converter_solicitacao_em_pedido(
        solicitacao_id=solicitacao.id,
        fornecedor_id=fornecedor.id,
        usuario=usuario,
    )

    solicitacao.refresh_from_db()
    assert pedido.status == PedidoCompra.Status.ABERTO
    assert pedido.itens.count() == 1
    assert solicitacao.status == SolicitacaoCompra.Status.CONVERTIDA


@pytest.mark.django_db
def test_recebimento_nao_excede_quantidade(usuario, produto, fornecedor):
    service = ComprasService()
    pedido = service.criar_pedido(
        fornecedor=fornecedor,
        usuario=usuario,
        itens=[{
            "produto": produto,
            "descricao": produto.nome,
            "quantidade": Decimal("3.0000"),
            "unidade_medida": produto.unidade_medida,
            "valor_unitario": Decimal("10.00"),
        }],
    )

    with pytest.raises(ValidationError):
        service.registrar_recebimento_parcial(
            pedido_id=pedido.id,
            usuario=usuario,
            itens=[{"item": pedido.itens.first().id, "quantidade": Decimal("4.0000")}],
        )
