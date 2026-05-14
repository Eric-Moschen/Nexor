from rest_framework import serializers

from apps.relatorios.models import ExportacaoArquivo, RelatorioGerado, RelatoriosRecord


class RelatoriosRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatoriosRecord
        fields = ("id", "name", "description", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class RelatorioGeradoSerializer(serializers.ModelSerializer):
    gerado_por_nome = serializers.CharField(source="gerado_por.get_full_name", read_only=True)

    class Meta:
        model = RelatorioGerado
        fields = ("id", "tipo_relatorio", "titulo", "filtros", "payload", "gerado_por", "gerado_por_nome", "created_at")
        read_only_fields = fields


class ExportacaoArquivoSerializer(serializers.ModelSerializer):
    solicitado_por_nome = serializers.CharField(source="solicitado_por.get_full_name", read_only=True)
    arquivo_url = serializers.SerializerMethodField()

    class Meta:
        model = ExportacaoArquivo
        fields = (
            "id",
            "relatorio",
            "tipo_relatorio",
            "formato",
            "status",
            "filtros",
            "arquivo",
            "arquivo_url",
            "erro",
            "task_id",
            "solicitado_por",
            "solicitado_por_nome",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields

    def get_arquivo_url(self, obj):
        if not obj.arquivo:
            return ""
        request = self.context.get("request")
        return request.build_absolute_uri(obj.arquivo.url) if request else obj.arquivo.url
