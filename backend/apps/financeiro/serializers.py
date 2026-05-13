from rest_framework import serializers

from apps.financeiro.models import FinanceiroRecord


class FinanceiroRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceiroRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
