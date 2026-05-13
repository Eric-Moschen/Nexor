from rest_framework import serializers

from apps.ordens_servico.models import ApontamentoHorasOS, HistoricoOS, ItemServico, MaterialUtilizadoOS, OrdemServico


class ItemServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemServico
        fields = ("id", "descricao", "quantidade", "valor_unitario", "valor_total", "observacao")
        read_only_fields = ("id", "valor_total")


class MaterialUtilizadoOSSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source="produto.nome", read_only=True)
    usuario_nome = serializers.CharField(source="usuario_responsavel.username", read_only=True)

    class Meta:
        model = MaterialUtilizadoOS
        fields = ("id", "produto", "produto_nome", "quantidade", "custo_unitario", "custo_total", "data_utilizacao", "usuario_nome")
        read_only_fields = ("id", "custo_total", "data_utilizacao", "usuario_nome")
        extra_kwargs = {"custo_unitario": {"required": False}}


class ApontamentoHorasOSSerializer(serializers.ModelSerializer):
    colaborador_nome = serializers.CharField(source="colaborador.username", read_only=True)

    class Meta:
        model = ApontamentoHorasOS
        fields = ("id", "colaborador", "colaborador_nome", "data", "hora_inicio", "hora_fim", "total_horas", "tipo_hora", "custo_hora", "custo_total", "observacao")
        read_only_fields = ("id", "total_horas", "custo_total", "colaborador_nome")


class HistoricoOSSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source="usuario_responsavel.username", read_only=True)

    class Meta:
        model = HistoricoOS
        fields = ("id", "tipo_evento", "descricao", "status_anterior", "status_novo", "usuario_nome", "dados_extras", "created_at")


class OrdemServicoSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(required=False, allow_blank=True)
    cliente_nome = serializers.CharField(source="cliente.razao_social", read_only=True)
    responsavel_nome = serializers.CharField(source="responsavel_tecnico.username", read_only=True)
    itens = ItemServicoSerializer(many=True, required=False)
    materiais = MaterialUtilizadoOSSerializer(many=True, read_only=True)
    apontamentos = ApontamentoHorasOSSerializer(many=True, read_only=True)
    historico = HistoricoOSSerializer(many=True, read_only=True)

    class Meta:
        model = OrdemServico
        fields = (
            "id",
            "numero",
            "cliente",
            "cliente_nome",
            "titulo",
            "descricao_servico",
            "tipo_servico",
            "prioridade",
            "status",
            "data_abertura",
            "data_prevista",
            "data_inicio",
            "data_finalizacao",
            "responsavel_tecnico",
            "responsavel_nome",
            "observacoes",
            "valor_estimado",
            "valor_final",
            "custo_materiais",
            "custo_mao_obra",
            "custo_total",
            "usuario_criador",
            "categoria_financeira",
            "centro_custo",
            "conta_receber",
            "nota_fiscal",
            "itens",
            "materiais",
            "apontamentos",
            "historico",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "status",
            "data_abertura",
            "data_inicio",
            "data_finalizacao",
            "valor_final",
            "custo_materiais",
            "custo_mao_obra",
            "custo_total",
            "usuario_criador",
            "conta_receber",
            "nota_fiscal",
            "created_at",
            "updated_at",
        )

    def validate_itens(self, value):
        for item in value:
            if item["quantidade"] <= 0:
                raise serializers.ValidationError("Quantidade do servico deve ser maior que zero.")
            if item["valor_unitario"] < 0:
                raise serializers.ValidationError("Valor unitario nao pode ser negativo.")
        return value


class FaturarOSSerializer(serializers.Serializer):
    data_vencimento = serializers.DateField(required=False)
    categoria = serializers.IntegerField(required=False)
    centro_custo = serializers.IntegerField(required=False)


class CancelarOSSerializer(serializers.Serializer):
    motivo = serializers.CharField(required=False, allow_blank=True)
