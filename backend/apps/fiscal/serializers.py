from rest_framework import serializers

from apps.fiscal.models import FiscalRecord


class FiscalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiscalRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
