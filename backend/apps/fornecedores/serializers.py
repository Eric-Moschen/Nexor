from rest_framework import serializers

from apps.fornecedores.models import FornecedoresRecord


class FornecedoresRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FornecedoresRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
