from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.fiscal.views import ClienteFiscalViewSet, EmpresaFiscalViewSet, FornecedorFiscalViewSet, NaturezaOperacaoViewSet, NotaFiscalViewSet, ProdutoFiscalViewSet

app_name = "fiscal"
router = DefaultRouter()
router.register("empresa", EmpresaFiscalViewSet, basename="empresa-fiscal")
router.register("clientes-fiscais", ClienteFiscalViewSet, basename="cliente-fiscal")
router.register("fornecedores-fiscais", FornecedorFiscalViewSet, basename="fornecedor-fiscal")
router.register("produtos-fiscais", ProdutoFiscalViewSet, basename="produto-fiscal")
router.register("naturezas-operacao", NaturezaOperacaoViewSet, basename="natureza-operacao")
router.register("nfe", NotaFiscalViewSet, basename="nota-fiscal")
urlpatterns = [path("", include(router.urls))]
