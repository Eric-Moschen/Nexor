from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.relatorios.views import (
    ExportacaoListAPIView,
    ExportarCSVView,
    ExportarExcelView,
    ExportarPDFView,
    RelatorioComercialView,
    RelatorioComprasView,
    RelatorioEstoqueView,
    RelatorioFinanceiroView,
    RelatorioOSView,
    RelatoriosRecordViewSet,
)

app_name = "relatorios"

router = DefaultRouter()
router.register("registros", RelatoriosRecordViewSet, basename="relatorios-record")

urlpatterns = [
    path("", include(router.urls)),
    path("financeiro/", RelatorioFinanceiroView.as_view(), name="relatorio-financeiro"),
    path("estoque/", RelatorioEstoqueView.as_view(), name="relatorio-estoque"),
    path("comercial/", RelatorioComercialView.as_view(), name="relatorio-comercial"),
    path("os/", RelatorioOSView.as_view(), name="relatorio-os"),
    path("compras/", RelatorioComprasView.as_view(), name="relatorio-compras"),
    path("exportar/pdf/", ExportarPDFView.as_view(), name="exportar-pdf"),
    path("exportar/excel/", ExportarExcelView.as_view(), name="exportar-excel"),
    path("exportar/csv/", ExportarCSVView.as_view(), name="exportar-csv"),
    path("exportacoes/", ExportacaoListAPIView.as_view(), name="exportacoes"),
]
