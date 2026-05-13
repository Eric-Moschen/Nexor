from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.ordens_servico.views import OrdensServicoRecordViewSet

app_name = "ordens_servico"
router = DefaultRouter()
router.register("registros", OrdensServicoRecordViewSet, basename="ordens_servico-record")
urlpatterns = [path("", include(router.urls))]
