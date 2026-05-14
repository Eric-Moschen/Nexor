import pytest
from django.core.exceptions import ValidationError
from django.test import override_settings

from apps.accounts.models import User
from apps.relatorios.enums import FormatoExportacao, TipoDashboard, TipoRelatorio
from apps.relatorios.models import DashboardCache, ExportacaoArquivo, RelatorioGerado
from apps.relatorios.services import DashboardService, RelatorioService
from apps.relatorios.validators import validar_periodo


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="bi-user", password="test12345", role=User.Role.ADMINISTRADOR)


@pytest.mark.django_db
@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}})
def test_consolidar_dashboard_usa_cache(usuario):
    service = DashboardService()
    service.dashboard_map[TipoDashboard.EXECUTIVO] = lambda filtros: {"total_recebido": "100.00"}

    payload = service.consolidar(tipo_dashboard=TipoDashboard.EXECUTIVO, filtros={}, usuario=usuario)
    payload_cache = service.consolidar(tipo_dashboard=TipoDashboard.EXECUTIVO, filtros={}, usuario=usuario)

    assert payload["indicadores"]["total_recebido"] == "100.00"
    assert payload_cache["indicadores"]["total_recebido"] == "100.00"
    assert DashboardCache.objects.filter(tipo_dashboard=TipoDashboard.EXECUTIVO).exists()


def test_validar_periodo_bloqueia_intervalo_invalido():
    with pytest.raises(ValidationError):
        validar_periodo("2026-05-20", "2026-05-01")


@pytest.mark.django_db
def test_gerar_relatorio_valido(usuario):
    service = RelatorioService()
    service.report_map[TipoRelatorio.FINANCEIRO] = ("Relatorio financeiro", lambda filtros: {"indicadores": {"receita_mensal": "0.00"}})

    relatorio = service.gerar_relatorio(tipo_relatorio=TipoRelatorio.FINANCEIRO, filtros={}, usuario=usuario)

    assert relatorio.tipo_relatorio == TipoRelatorio.FINANCEIRO
    assert RelatorioGerado.objects.filter(id=relatorio.id).exists()


@pytest.mark.django_db
def test_exportar_csv(usuario):
    service = RelatorioService()
    service.report_map[TipoRelatorio.FINANCEIRO] = ("Relatorio financeiro", lambda filtros: {"indicadores": {"receita_mensal": "0.00"}})

    exportacao = service.solicitar_exportacao(tipo_relatorio=TipoRelatorio.FINANCEIRO, formato=FormatoExportacao.CSV, filtros={}, usuario=usuario)

    assert exportacao.status == "concluida"
    assert exportacao.arquivo.name.endswith(".csv")
    assert ExportacaoArquivo.objects.filter(id=exportacao.id).exists()
