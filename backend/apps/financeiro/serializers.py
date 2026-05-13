from rest_framework import serializers

from apps.financeiro.enums import TipoBaixa, TipoFinanceiro
from apps.financeiro.models import BaixaFinanceira, CategoriaFinanceira, CentroCusto, ContaPagar, ContaReceber, Parcelamento


class CentroCustoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroCusto
        fields = ("id", "codigo", "nome", "descricao", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class CategoriaFinanceiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaFinanceira
        fields = ("id", "nome", "tipo", "descricao", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class ContaPagarSerializer(serializers.ModelSerializer):
    fornecedor_nome = serializers.CharField(source="fornecedor.razao_social", read_only=True)
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    centro_custo_nome = serializers.CharField(source="centro_custo.nome", read_only=True)

    class Meta:
        model = ContaPagar
        fields = (
            "id",
            "numero_lancamento",
            "fornecedor",
            "fornecedor_nome",
            "descricao",
            "categoria",
            "categoria_nome",
            "centro_custo",
            "centro_custo_nome",
            "valor_original",
            "valor_atual",
            "data_emissao",
            "data_vencimento",
            "status",
            "tipo_pagamento",
            "observacao",
            "pedido_compra_origem",
            "usuario_responsavel",
            "parcelamento",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "numero_lancamento", "valor_atual", "status", "usuario_responsavel", "created_at", "updated_at")

    def validate_categoria(self, value):
        if value.tipo != TipoFinanceiro.DESPESA:
            raise serializers.ValidationError("Conta a pagar exige categoria de despesa.")
        return value


class ContaReceberSerializer(serializers.ModelSerializer):
    cliente_nome = serializers.CharField(source="cliente.razao_social", read_only=True)
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    centro_custo_nome = serializers.CharField(source="centro_custo.nome", read_only=True)

    class Meta:
        model = ContaReceber
        fields = (
            "id",
            "numero_lancamento",
            "cliente",
            "cliente_nome",
            "descricao",
            "categoria",
            "categoria_nome",
            "centro_custo",
            "centro_custo_nome",
            "valor_original",
            "valor_atual",
            "data_emissao",
            "data_vencimento",
            "status",
            "forma_recebimento",
            "observacao",
            "usuario_responsavel",
            "parcelamento",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "numero_lancamento", "valor_atual", "status", "usuario_responsavel", "created_at", "updated_at")

    def validate_categoria(self, value):
        if value.tipo != TipoFinanceiro.RECEITA:
            raise serializers.ValidationError("Conta a receber exige categoria de receita.")
        return value


class BaixaFinanceiraSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaixaFinanceira
        fields = (
            "id",
            "conta_pagar",
            "conta_receber",
            "tipo",
            "valor_pago",
            "data_pagamento",
            "multa",
            "juros",
            "desconto",
            "observacao",
            "usuario_responsavel",
            "created_at",
        )
        read_only_fields = ("id", "conta_pagar", "conta_receber", "tipo", "usuario_responsavel", "created_at")


class BaixaInputSerializer(serializers.Serializer):
    valor_pago = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0)
    data_pagamento = serializers.DateField()
    multa = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0, required=False, default=0)
    juros = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0, required=False, default=0)
    desconto = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=0, required=False, default=0)
    observacao = serializers.CharField(required=False, allow_blank=True)

    def validate_valor_pago(self, value):
        if value <= 0:
            raise serializers.ValidationError("Valor da baixa deve ser maior que zero.")
        return value


class ParcelamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelamento
        fields = ("id", "descricao", "quantidade_parcelas", "valor_total", "data_primeiro_vencimento", "intervalo_meses")
        read_only_fields = ("id",)


class FluxoCaixaSerializer(serializers.Serializer):
    total_pago = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_recebido = serializers.DecimalField(max_digits=14, decimal_places=2)
    saldo = serializers.DecimalField(max_digits=14, decimal_places=2)
