from rest_framework import serializers

from apps.clientes.serializers import ContatoRelacionamentoSerializer, EnderecoRelacionamentoSerializer
from apps.fornecedores.models import Fornecedor


class FornecedorSerializer(serializers.ModelSerializer):
    enderecos = EnderecoRelacionamentoSerializer(many=True, required=False)
    contatos = ContatoRelacionamentoSerializer(many=True, required=False)

    class Meta:
        model = Fornecedor
        fields = (
            "id",
            "tipo_pessoa",
            "razao_social",
            "nome_fantasia",
            "documento",
            "inscricao_estadual",
            "email",
            "telefone",
            "whatsapp",
            "categoria",
            "status",
            "observacoes",
            "usuario_responsavel",
            "enderecos",
            "contatos",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
