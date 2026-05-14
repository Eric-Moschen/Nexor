from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", include("apps.core.urls")),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/v1/accounts/", include("apps.accounts.urls")),
    path("api/v1/estoque/", include("apps.estoque.urls")),
    path("api/v1/compras/", include("apps.compras.urls")),
    path("api/v1/financeiro/", include("apps.financeiro.urls")),
    path("api/v1/fiscal/", include("apps.fiscal.urls")),
    path("api/v1/os/", include("apps.ordens_servico.urls")),
    path("api/v1/orcamentos/", include("apps.orcamentos.urls")),
    path("api/v1/clientes/", include("apps.clientes.urls")),
    path("api/v1/crm/", include("apps.clientes.crm_urls")),
    path("api/v1/fornecedores/", include("apps.fornecedores.urls")),
    path("api/v1/dashboard/", include("apps.relatorios.dashboard_urls")),
    path("api/v1/relatorios/", include("apps.relatorios.urls")),
    path("api/v1/auditoria/", include("apps.auditoria.urls")),
]
