from rest_framework import serializers

from apps.clientes.models import ClientesRecord


class ClientesRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientesRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
