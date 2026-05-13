from rest_framework import serializers

from apps.fiscal.models import (
    ClienteFiscal,
    EmpresaFiscal,
    EventoFiscal,
    FornecedorFiscal,
    ItemNotaFiscal,
    NaturezaOperacao,
    NotaFiscal,
    ProdutoFiscal,
)


class EmpresaFiscalSerializer(serializers.ModelSerializer):
    senha_certificado = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = EmpresaFiscal
        fields = (
            "id",
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "inscricao_estadual",
            "inscricao_municipal",
            "regime_tributario",
            "cnae",
            "endereco_fiscal",
            "municipio_ibge",
            "uf",
            "cep",
            "certificado_a1",
            "senha_certificado",
            "ambiente",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class ClienteFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteFiscal
        fields = "__all__"


class FornecedorFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FornecedorFiscal
        fields = "__all__"


class ProdutoFiscalSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)

    class Meta:
        model = ProdutoFiscal
        fields = "__all__"


class NaturezaOperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturezaOperacao
        fields = ("id", "codigo", "descricao", "tipo_operacao", "cfop_padrao", "movimenta_estoque", "gera_financeiro", "is_active")


class ItemNotaFiscalSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)

    class Meta:
        model = ItemNotaFiscal
        fields = (
            "id",
            "produto",
            "produto_nome",
            "descricao",
            "cfop",
            "ncm",
            "cst_csosn",
            "quantidade",
            "valor_unitario",
            "valor_total",
            "desconto",
            "base_icms",
            "valor_icms",
            "base_pis",
            "valor_pis",
            "base_cofins",
            "valor_cofins",
            "base_ipi",
            "valor_ipi",
        )
        read_only_fields = ("id", "valor_total", "base_icms", "valor_icms", "base_pis", "valor_pis", "base_cofins", "valor_cofins", "base_ipi", "valor_ipi")


class NotaFiscalSerializer(serializers.ModelSerializer):
    itens = ItemNotaFiscalSerializer(many=True)
    eventos = serializers.SerializerMethodField()

    class Meta:
        model = NotaFiscal
        fields = (
            "id",
            "numero",
            "serie",
            "chave_acesso",
            "protocolo",
            "ambiente",
            "tipo_emissao",
            "tipo_operacao",
            "natureza_operacao",
            "emitente",
            "destinatario_cliente",
            "destinatario_fornecedor",
            "data_emissao",
            "data_saida_entrada",
            "status",
            "valor_produtos",
            "valor_frete",
            "valor_desconto",
            "valor_total",
            "motivo_rejeicao",
            "usuario_responsavel",
            "categoria_financeira",
            "centro_custo",
            "itens",
            "eventos",
        )
        read_only_fields = ("id", "chave_acesso", "protocolo", "data_emissao", "status", "valor_produtos", "valor_total", "motivo_rejeicao", "usuario_responsavel")

    def get_eventos(self, obj):
        return EventoFiscalSerializer(obj.eventos.all()[:20], many=True).data

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError("NFe precisa ter ao menos um item.")
        return value

    def validate(self, attrs):
        cliente = attrs.get("destinatario_cliente") or getattr(self.instance, "destinatario_cliente", None)
        fornecedor = attrs.get("destinatario_fornecedor") or getattr(self.instance, "destinatario_fornecedor", None)
        if not cliente and not fornecedor:
            raise serializers.ValidationError("Informe cliente ou fornecedor destinatario.")
        return attrs


class EventoFiscalSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source="usuario_responsavel.username", read_only=True)

    class Meta:
        model = EventoFiscal
        fields = ("id", "tipo_evento", "codigo_retorno", "mensagem", "protocolo", "xml_retorno", "data_evento", "usuario_nome")


class CancelamentoNFeSerializer(serializers.Serializer):
    justificativa = serializers.CharField()

    def validate_justificativa(self, value):
        if len(value.strip()) < 15:
            raise serializers.ValidationError("Justificativa de cancelamento deve ter ao menos 15 caracteres.")
        return value
