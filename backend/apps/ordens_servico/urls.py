from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.ordens_servico.views import OrdemServicoViewSet

app_name = "ordens_servico"
router = DefaultRouter()
router.register("", OrdemServicoViewSet, basename="ordem-servico")
urlpatterns = [path("", include(router.urls))]
