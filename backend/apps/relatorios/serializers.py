from rest_framework import serializers

from apps.relatorios.models import RelatoriosRecord


class RelatoriosRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatoriosRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
