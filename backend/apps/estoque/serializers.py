from rest_framework import serializers

from apps.estoque.models import EstoqueRecord


class EstoqueRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstoqueRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
