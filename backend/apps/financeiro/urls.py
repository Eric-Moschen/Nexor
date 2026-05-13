from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.financeiro.views import (
    CategoriaFinanceiraViewSet,
    CentroCustoViewSet,
    ContaPagarViewSet,
    ContaReceberViewSet,
    DashboardFinanceiroView,
    FluxoCaixaView,
)

app_name = "financeiro"
router = DefaultRouter()
router.register("contas-pagar", ContaPagarViewSet, basename="conta-pagar")
router.register("contas-receber", ContaReceberViewSet, basename="conta-receber")
router.register("centros-custo", CentroCustoViewSet, basename="centro-custo")
router.register("categorias", CategoriaFinanceiraViewSet, basename="categoria-financeira")

urlpatterns = [
    path("", include(router.urls)),
    path("fluxo-caixa/", FluxoCaixaView.as_view(), name="fluxo-caixa"),
    path("dashboard/", DashboardFinanceiroView.as_view(), name="dashboard"),
]
