from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.compras.views import PedidoCompraViewSet, SolicitacaoCompraViewSet

app_name = "compras"
router = DefaultRouter()
router.register("solicitacoes", SolicitacaoCompraViewSet, basename="solicitacao-compra")
router.register("pedidos", PedidoCompraViewSet, basename="pedido-compra")
urlpatterns = [path("", include(router.urls))]
