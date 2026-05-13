from rest_framework import serializers

from apps.fornecedores.models import Fornecedor


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = (
            "id",
            "razao_social",
            "nome_fantasia",
            "documento",
            "email",
            "telefone",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
