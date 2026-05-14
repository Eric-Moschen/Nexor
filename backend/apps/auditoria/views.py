from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.accounts.permissions import has_permission
from apps.auditoria.serializers import AuditoriaRecordSerializer
from apps.auditoria.selectors import list_records
from apps.core.models import AuditLog
from apps.core.serializers import AuditLogSerializer


class AuditoriaRecordViewSet(ModelViewSet):
    serializer_class = AuditoriaRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return list_records()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AuditLogViewSet(ReadOnlyModelViewSet):
    serializer_class = AuditLogSerializer
    permission_classes = [has_permission("auditoria.logs.visualizar")]
    filterset_fields = ("action", "module", "record_model")
    search_fields = ("record_repr", "record_id", "module", "record_model")
    ordering_fields = ("created_at",)

    def get_queryset(self):
        return AuditLog.objects.select_related("user").all()
