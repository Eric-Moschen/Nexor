from rest_framework import serializers

from apps.orcamentos.models import HistoricoOrcamento, ItemProdutoOrcamento, ItemServicoOrcamento, Orcamento


class ItemProdutoOrcamentoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)

    class Meta:
        model = ItemProdutoOrcamento
        fields = ("id", "produto", "produto_nome", "descricao", "quantidade", "custo_unitario", "valor_unitario", "desconto", "valor_total", "custo_total")
        read_only_fields = ("id", "valor_total", "custo_total", "produto_nome")
        extra_kwargs = {"custo_unitario": {"required": False}}


class ItemServicoOrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemServicoOrcamento
        fields = ("id", "descricao", "quantidade", "custo_estimado", "valor_unitario", "desconto", "valor_total", "observacao")
        read_only_fields = ("id", "valor_total")


class HistoricoOrcamentoSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source="usuario_responsavel.username", read_only=True)

    class Meta:
        model = HistoricoOrcamento
        fields = ("id", "tipo_evento", "descricao", "status_anterior", "status_novo", "usuario_nome", "dados_extras", "created_at")


class OrcamentoSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(required=False, allow_blank=True)
    cliente_nome = serializers.CharField(source="cliente.razao_social", read_only=True)
    usuario_nome = serializers.CharField(source="usuario_responsavel.username", read_only=True)
    itens_produto = ItemProdutoOrcamentoSerializer(many=True, required=False)
    itens_servico = ItemServicoOrcamentoSerializer(many=True, required=False)
    historico = HistoricoOrcamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Orcamento
        fields = (
            "id",
            "numero",
            "cliente",
            "cliente_nome",
            "titulo",
            "descricao",
            "data_criacao",
            "data_validade",
            "status",
            "condicao_pagamento",
            "prazo_entrega",
            "observacoes_internas",
            "observacoes_cliente",
            "valor_produtos",
            "valor_servicos",
            "valor_desconto",
            "valor_total",
            "custo_total",
            "margem_estimada",
            "motivo_reprovacao",
            "usuario_responsavel",
            "usuario_nome",
            "ordem_servico",
            "pdf_gerado",
            "itens_produto",
            "itens_servico",
            "historico",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "data_criacao",
            "status",
            "valor_produtos",
            "valor_servicos",
            "valor_total",
            "custo_total",
            "margem_estimada",
            "motivo_reprovacao",
            "usuario_responsavel",
            "ordem_servico",
            "pdf_gerado",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        itens_produto = attrs.get("itens_produto", [])
        itens_servico = attrs.get("itens_servico", [])
        if not self.instance and not itens_produto and not itens_servico:
            raise serializers.ValidationError("Orcamento precisa ter ao menos um item.")
        return attrs


class ReprovarOrcamentoSerializer(serializers.Serializer):
    motivo = serializers.CharField()

    def validate_motivo(self, value):
        if not value.strip():
            raise serializers.ValidationError("Reprovacao exige motivo.")
        return value


class CancelarOrcamentoSerializer(serializers.Serializer):
    motivo = serializers.CharField(required=False, allow_blank=True)
