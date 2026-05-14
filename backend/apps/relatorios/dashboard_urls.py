from django.urls import path

from apps.relatorios.views import DashboardComercialView, DashboardEstoqueView, DashboardExecutivoView, DashboardFinanceiroView, DashboardOperacionalView

app_name = "dashboard"

urlpatterns = [
    path("executivo/", DashboardExecutivoView.as_view(), name="dashboard-executivo"),
    path("financeiro/", DashboardFinanceiroView.as_view(), name="dashboard-financeiro"),
    path("estoque/", DashboardEstoqueView.as_view(), name="dashboard-estoque"),
    path("comercial/", DashboardComercialView.as_view(), name="dashboard-comercial"),
    path("operacional/", DashboardOperacionalView.as_view(), name="dashboard-operacional"),
]
