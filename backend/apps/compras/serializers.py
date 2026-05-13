from rest_framework import serializers

from apps.compras.models import ItemPedidoCompra, ItemSolicitacaoCompra, PedidoCompra, SolicitacaoCompra


class ItemSolicitacaoCompraSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)
    unidade_medida_sigla = serializers.CharField(source="unidade_medida.sigla", read_only=True)

    class Meta:
        model = ItemSolicitacaoCompra
        fields = (
            "id",
            "produto",
            "produto_nome",
            "descricao_livre",
            "quantidade_solicitada",
            "unidade_medida",
            "unidade_medida_sigla",
            "observacao",
            "status",
        )
        read_only_fields = ("id", "status")

    def validate(self, attrs):
        produto = attrs.get("produto")
        descricao_livre = attrs.get("descricao_livre", "")
        if not produto and not descricao_livre.strip():
            raise serializers.ValidationError("Informe um produto ou uma descricao livre.")
        return attrs


class SolicitacaoCompraSerializer(serializers.ModelSerializer):
    itens = ItemSolicitacaoCompraSerializer(many=True)
    solicitante_nome = serializers.CharField(source="solicitante.username", read_only=True)
    aprovador_nome = serializers.CharField(source="aprovador.username", read_only=True)

    class Meta:
        model = SolicitacaoCompra
        fields = (
            "id",
            "numero",
            "solicitante",
            "solicitante_nome",
            "centro_custo",
            "justificativa",
            "prioridade",
            "status",
            "data_solicitacao",
            "data_aprovacao",
            "aprovador",
            "aprovador_nome",
            "observacoes",
            "itens",
        )
        read_only_fields = ("id", "numero", "solicitante", "status", "data_solicitacao", "data_aprovacao", "aprovador")

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError("A solicitacao precisa ter pelo menos um item.")
        return value


class ItemPedidoCompraSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)
    unidade_medida_sigla = serializers.CharField(source="unidade_medida.sigla", read_only=True)

    class Meta:
        model = ItemPedidoCompra
        fields = (
            "id",
            "produto",
            "produto_nome",
            "descricao",
            "quantidade",
            "unidade_medida",
            "unidade_medida_sigla",
            "valor_unitario",
            "valor_total",
            "quantidade_recebida",
        )
        read_only_fields = ("id", "valor_total", "quantidade_recebida")

    def validate_valor_unitario(self, value):
        if value < 0:
            raise serializers.ValidationError("Valor unitario nao pode ser negativo.")
        return value


class PedidoCompraSerializer(serializers.ModelSerializer):
    itens = ItemPedidoCompraSerializer(many=True)
    fornecedor_nome = serializers.CharField(source="fornecedor.razao_social", read_only=True)

    class Meta:
        model = PedidoCompra
        fields = (
            "id",
            "numero",
            "solicitacao_origem",
            "fornecedor",
            "fornecedor_nome",
            "data_pedido",
            "previsao_entrega",
            "status",
            "valor_total",
            "observacoes",
            "itens",
        )
        read_only_fields = ("id", "numero", "data_pedido", "status", "valor_total")

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError("O pedido precisa ter pelo menos um item.")
        return value


class ReprovacaoSerializer(serializers.Serializer):
    motivo = serializers.CharField()

    def validate_motivo(self, value):
        if not value.strip():
            raise serializers.ValidationError("Reprovacao exige motivo.")
        return value


class ConverterPedidoSerializer(serializers.Serializer):
    fornecedor = serializers.IntegerField()
    previsao_entrega = serializers.DateField(required=False, allow_null=True)
    observacoes = serializers.CharField(required=False, allow_blank=True)


class RecebimentoItemSerializer(serializers.Serializer):
    item = serializers.IntegerField()
    quantidade = serializers.DecimalField(max_digits=14, decimal_places=4, min_value=0)

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantidade recebida deve ser maior que zero.")
        return value


class RecebimentoParcialSerializer(serializers.Serializer):
    itens = RecebimentoItemSerializer(many=True)
    observacao = serializers.CharField(required=False, allow_blank=True)

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError("Informe ao menos um item recebido.")
        return value
