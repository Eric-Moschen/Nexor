from rest_framework import serializers

from apps.clientes.models import Cliente, ContatoRelacionamento, DocumentoRelacionamento, EnderecoRelacionamento, HistoricoRelacionamento, InteracaoCRM


class EnderecoRelacionamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoRelacionamento
        fields = (
            "id",
            "cep",
            "rua",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "uf",
            "codigo_ibge",
            "tipo",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class ContatoRelacionamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContatoRelacionamento
        fields = (
            "id",
            "nome",
            "cargo",
            "email",
            "telefone",
            "whatsapp",
            "observacao",
            "principal",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class DocumentoRelacionamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoRelacionamento
        fields = (
            "id",
            "tipo_documento",
            "titulo",
            "arquivo",
            "observacao",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class HistoricoRelacionamentoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source="usuario_responsavel.get_full_name", read_only=True)

    class Meta:
        model = HistoricoRelacionamento
        fields = (
            "id",
            "tipo_evento",
            "descricao",
            "usuario_responsavel",
            "usuario_nome",
            "dados_extras",
            "created_at",
        )
        read_only_fields = fields


class InteracaoCRMSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source="cliente.razao_social", read_only=True)
    responsavel_nome = serializers.CharField(source="responsavel.get_full_name", read_only=True)

    class Meta:
        model = InteracaoCRM
        fields = (
            "id",
            "cliente",
            "cliente_nome",
            "tipo_interacao",
            "descricao",
            "responsavel",
            "responsavel_nome",
            "data",
            "proximo_contato",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "cliente_nome", "responsavel_nome", "created_at", "updated_at")


class ClienteSerializer(serializers.ModelSerializer):
    enderecos = EnderecoRelacionamentoSerializer(many=True, required=False)
    contatos = ContatoRelacionamentoSerializer(many=True, required=False)

    class Meta:
        model = Cliente
        fields = (
            "id",
            "tipo_pessoa",
            "razao_social",
            "nome_fantasia",
            "documento",
            "inscricao_estadual",
            "inscricao_municipal",
            "email",
            "telefone",
            "whatsapp",
            "status",
            "limite_credito",
            "observacoes",
            "usuario_responsavel",
            "enderecos",
            "contatos",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
