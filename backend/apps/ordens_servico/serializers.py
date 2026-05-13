from rest_framework import serializers

from apps.ordens_servico.models import OrdensServicoRecord


class OrdensServicoRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdensServicoRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
