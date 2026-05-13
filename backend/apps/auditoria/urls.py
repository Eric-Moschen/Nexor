from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.auditoria.views import AuditoriaRecordViewSet

app_name = "auditoria"
router = DefaultRouter()
router.register("registros", AuditoriaRecordViewSet, basename="auditoria-record")
urlpatterns = [path("", include(router.urls))]
