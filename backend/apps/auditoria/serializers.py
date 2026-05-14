from rest_framework import serializers

from apps.auditoria.models import AuditoriaRecord
from apps.core.serializers import AuditLogSerializer


class AuditoriaRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditoriaRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
