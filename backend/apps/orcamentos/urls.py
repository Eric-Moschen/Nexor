from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.orcamentos.views import OrcamentoViewSet

app_name = "orcamentos"
router = DefaultRouter()
router.register("", OrcamentoViewSet, basename="orcamento")
urlpatterns = [path("", include(router.urls))]
