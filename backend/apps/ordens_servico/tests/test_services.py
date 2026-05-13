from datetime import date, time
from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.clientes.models import Cliente
from apps.estoque.models import CategoriaProduto, Produto, UnidadeMedida
from apps.financeiro.enums import TipoFinanceiro
from apps.financeiro.models import CategoriaFinanceira, CentroCusto
from apps.ordens_servico.enums import StatusOS, TipoHoraOS
from apps.ordens_servico.services import OrdemServicoService


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="operacional-os", password="test12345", role=User.Role.OPERACIONAL)


@pytest.fixture
def supervisor(db):
    return User.objects.create_user(username="supervisor-os", password="test12345", role=User.Role.SUPERVISOR)


@pytest.fixture
def cliente(db):
    return Cliente.objects.create(razao_social="Cliente OS", documento="12345678000195")


@pytest.fixture
def produto(db):
    categoria = CategoriaProduto.objects.create(nome="Materiais OS")
    unidade = UnidadeMedida.objects.create(sigla="UNOS", nome="Unidade OS")
    return Produto.objects.create(
        codigo_interno="OS-MAT-001",
        sku="OS-MAT-SKU",
        nome="Chapa para servico",
        categoria=categoria,
        unidade_medida=unidade,
        custo_medio=Decimal("12.5000"),
        estoque_atual=Decimal("10.0000"),
    )


@pytest.fixture
def categoria_receita(db):
    return CategoriaFinanceira.objects.create(nome="Servico prestado", tipo=TipoFinanceiro.RECEITA)


@pytest.fixture
def centro(db):
    return CentroCusto.objects.create(codigo="OS", nome="Ordens de Servico")


def criar_os_base(usuario, cliente, **extra):
    dados = {
        "cliente": cliente,
        "titulo": "Instalacao industrial",
        "descricao_servico": "Instalacao com material e mao de obra",
        "tipo_servico": "Instalacao",
        "valor_estimado": Decimal("1000.00"),
    }
    dados.update(extra)
    return OrdemServicoService().criar_os(usuario=usuario, **dados)


@pytest.mark.django_db
def test_criar_os_valida(usuario, cliente):
    ordem = criar_os_base(usuario, cliente)

    assert ordem.numero.startswith("OS-")
    assert ordem.status == StatusOS.RASCUNHO
    assert ordem.usuario_criador == usuario


@pytest.mark.django_db
def test_fluxo_aprovar_iniciar_pausar_retomar_finalizar(usuario, supervisor, cliente):
    service = OrdemServicoService()
    ordem = criar_os_base(usuario, cliente)

    service.enviar_aprovacao(ordem_id=ordem.id, usuario=usuario)
    service.aprovar(ordem_id=ordem.id, usuario=supervisor)
    service.iniciar(ordem_id=ordem.id, usuario=usuario)
    service.pausar(ordem_id=ordem.id, usuario=supervisor)
    service.retomar(ordem_id=ordem.id, usuario=supervisor)
    ordem = service.finalizar(ordem_id=ordem.id, usuario=supervisor)

    assert ordem.status == StatusOS.FINALIZADA
    assert ordem.data_finalizacao is not None


@pytest.mark.django_db
def test_bloquear_edicao_de_os_finalizada(usuario, supervisor, cliente):
    service = OrdemServicoService()
    ordem = criar_os_base(usuario, cliente)
    service.enviar_aprovacao(ordem_id=ordem.id, usuario=usuario)
    service.aprovar(ordem_id=ordem.id, usuario=supervisor)
    ordem = service.finalizar(ordem_id=ordem.id, usuario=supervisor)

    with pytest.raises(ValidationError):
        service.adicionar_item_servico(ordem_id=ordem.id, usuario=usuario, descricao="Servico extra", quantidade=Decimal("1.0000"), valor_unitario=Decimal("50.00"))


@pytest.mark.django_db
def test_adicionar_material_com_saldo_registra_saida(usuario, cliente, produto):
    ordem = criar_os_base(usuario, cliente)
    material = OrdemServicoService().adicionar_material(ordem_id=ordem.id, produto=produto, quantidade=Decimal("2.0000"), usuario=usuario)
    produto.refresh_from_db()

    assert material.custo_total == Decimal("25.00")
    assert produto.estoque_atual == Decimal("8.0000")


@pytest.mark.django_db
def test_bloquear_material_sem_saldo(usuario, cliente, produto):
    ordem = criar_os_base(usuario, cliente)

    with pytest.raises(ValidationError):
        OrdemServicoService().adicionar_material(ordem_id=ordem.id, produto=produto, quantidade=Decimal("20.0000"), usuario=usuario)


@pytest.mark.django_db
def test_registrar_apontamento_valido(usuario, cliente):
    ordem = criar_os_base(usuario, cliente)
    apontamento = OrdemServicoService().registrar_apontamento(
        ordem_id=ordem.id,
        colaborador=usuario,
        data=date(2026, 5, 13),
        hora_inicio=time(8, 0),
        hora_fim=time(10, 30),
        tipo_hora=TipoHoraOS.NORMAL,
        custo_hora=Decimal("40.00"),
        usuario=usuario,
    )

    assert apontamento.total_horas == Decimal("2.50")
    assert apontamento.custo_total == Decimal("100.00")


@pytest.mark.django_db
def test_bloquear_hora_fim_menor_que_inicio(usuario, cliente):
    ordem = criar_os_base(usuario, cliente)

    with pytest.raises(ValidationError):
        OrdemServicoService().registrar_apontamento(
            ordem_id=ordem.id,
            colaborador=usuario,
            data=date(2026, 5, 13),
            hora_inicio=time(10, 0),
            hora_fim=time(9, 0),
            usuario=usuario,
        )


@pytest.mark.django_db
def test_bloquear_sobreposicao_de_apontamento(usuario, cliente):
    service = OrdemServicoService()
    ordem = criar_os_base(usuario, cliente)
    service.registrar_apontamento(ordem_id=ordem.id, colaborador=usuario, data=date(2026, 5, 13), hora_inicio=time(8, 0), hora_fim=time(10, 0), usuario=usuario)

    with pytest.raises(ValidationError):
        service.registrar_apontamento(ordem_id=ordem.id, colaborador=usuario, data=date(2026, 5, 13), hora_inicio=time(9, 0), hora_fim=time(11, 0), usuario=usuario)


@pytest.mark.django_db
def test_faturar_os_gera_conta_receber_e_bloqueia_duplicidade(usuario, supervisor, cliente, categoria_receita, centro):
    service = OrdemServicoService()
    ordem = criar_os_base(usuario, cliente, categoria_financeira=categoria_receita, centro_custo=centro)
    service.enviar_aprovacao(ordem_id=ordem.id, usuario=usuario)
    service.aprovar(ordem_id=ordem.id, usuario=supervisor)
    service.finalizar(ordem_id=ordem.id, usuario=supervisor)
    ordem = service.faturar(ordem_id=ordem.id, usuario=usuario, data_vencimento=date(2026, 5, 30))

    assert ordem.status == StatusOS.FATURADA
    assert ordem.conta_receber is not None
    with pytest.raises(ValidationError):
        service.faturar(ordem_id=ordem.id, usuario=usuario, data_vencimento=date(2026, 5, 30))


@pytest.mark.django_db
def test_os_cancelada_nao_gera_financeiro(usuario, cliente, categoria_receita, centro):
    service = OrdemServicoService()
    ordem = criar_os_base(usuario, cliente, categoria_financeira=categoria_receita, centro_custo=centro)
    service.cancelar(ordem_id=ordem.id, usuario=usuario)

    with pytest.raises(ValidationError):
        service.faturar(ordem_id=ordem.id, usuario=usuario, data_vencimento=date(2026, 5, 30))
