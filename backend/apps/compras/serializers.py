from rest_framework import serializers

from apps.compras.models import ComprasRecord


class ComprasRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprasRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
