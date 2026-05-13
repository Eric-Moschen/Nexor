from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.estoque.views import CategoriaProdutoViewSet, MovimentacaoEstoqueViewSet, ProdutoViewSet, UnidadeMedidaViewSet

app_name = "estoque"
router = DefaultRouter()
router.register("produtos", ProdutoViewSet, basename="produto")
router.register("categorias", CategoriaProdutoViewSet, basename="categoria")
router.register("unidades-medida", UnidadeMedidaViewSet, basename="unidade-medida")
router.register("movimentacoes", MovimentacaoEstoqueViewSet, basename="movimentacao")
urlpatterns = [path("", include(router.urls))]
