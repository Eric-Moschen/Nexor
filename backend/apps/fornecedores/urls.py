from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.fornecedores.views import FornecedorViewSet

app_name = "fornecedores"
router = DefaultRouter()
router.register("", FornecedorViewSet, basename="fornecedor")
router.register("fornecedores", FornecedorViewSet, basename="fornecedor-legado")
urlpatterns = [path("", include(router.urls))]
