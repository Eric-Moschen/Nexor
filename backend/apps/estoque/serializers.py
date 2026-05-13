from rest_framework import serializers

from apps.estoque.models import CategoriaProduto, MovimentacaoEstoque, Produto, UnidadeMedida


class CategoriaProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaProduto
        fields = ("id", "nome", "descricao", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ("id", "sigla", "nome", "descricao", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    unidade_medida_sigla = serializers.CharField(source="unidade_medida.sigla", read_only=True)

    class Meta:
        model = Produto
        fields = (
            "id",
            "codigo_interno",
            "sku",
            "codigo_barras",
            "nome",
            "descricao",
            "categoria",
            "categoria_nome",
            "unidade_medida",
            "unidade_medida_sigla",
            "marca",
            "custo_medio",
            "preco_venda",
            "estoque_minimo",
            "estoque_atual",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "estoque_atual", "created_at", "updated_at")

    def validate(self, attrs):
        categoria = attrs.get("categoria", getattr(self.instance, "categoria", None))
        unidade_medida = attrs.get("unidade_medida", getattr(self.instance, "unidade_medida", None))
        if categoria and not categoria.is_active:
            raise serializers.ValidationError({"categoria": "Categoria inativa nao pode ser usada."})
        if unidade_medida and not unidade_medida.is_active:
            raise serializers.ValidationError({"unidade_medida": "Unidade de medida inativa nao pode ser usada."})
        return attrs


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)
    usuario_responsavel_nome = serializers.CharField(source="usuario_responsavel.username", read_only=True)

    class Meta:
        model = MovimentacaoEstoque
        fields = (
            "id",
            "produto",
            "produto_nome",
            "tipo",
            "quantidade",
            "saldo_anterior",
            "saldo_posterior",
            "usuario_responsavel",
            "usuario_responsavel_nome",
            "observacao",
            "data_movimentacao",
        )
        read_only_fields = (
            "id",
            "tipo",
            "saldo_anterior",
            "saldo_posterior",
            "usuario_responsavel",
            "data_movimentacao",
        )


class EstoqueMovimentacaoInputSerializer(serializers.Serializer):
    produto = serializers.PrimaryKeyRelatedField(queryset=Produto.objects.filter(is_active=True))
    quantidade = serializers.DecimalField(max_digits=14, decimal_places=4, min_value=0)
    observacao = serializers.CharField(required=False, allow_blank=True)

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value
