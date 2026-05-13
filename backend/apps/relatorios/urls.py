from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.relatorios.views import RelatoriosRecordViewSet

app_name = "relatorios"
router = DefaultRouter()
router.register("registros", RelatoriosRecordViewSet, basename="relatorios-record")
urlpatterns = [path("", include(router.urls))]
