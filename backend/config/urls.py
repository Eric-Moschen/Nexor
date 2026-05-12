"""Root URL configuration for Nexor ERP."""
from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok", "service": "nexor-api"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", HealthCheckView.as_view(), name="health-check"),
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/estoque/", include("apps.estoque.urls")),
    path("api/v1/compras/", include("apps.compras.urls")),
    path("api/v1/financeiro/", include("apps.financeiro.urls")),
    path("api/v1/fiscal/", include("apps.fiscal.urls")),
    path("api/v1/os/", include("apps.ordens_servico.urls")),
    path("api/v1/clientes/", include("apps.clientes.urls")),
    path("api/v1/fornecedores/", include("apps.fornecedores.urls")),
    path("api/v1/relatorios/", include("apps.relatorios.urls")),
]
