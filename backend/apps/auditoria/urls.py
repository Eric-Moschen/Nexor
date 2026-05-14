from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.auditoria.views import AuditLogViewSet, AuditoriaRecordViewSet

app_name = "auditoria"
router = DefaultRouter()
router.register("registros", AuditoriaRecordViewSet, basename="auditoria-record")
router.register("logs", AuditLogViewSet, basename="audit-log")
urlpatterns = [path("", include(router.urls))]
