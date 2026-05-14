from apps.relatorios.models import DashboardCache, ExportacaoArquivo, RelatorioGerado


class DashboardCacheRepository:
    def get_for_update(self, chave):
        return DashboardCache.objects.select_for_update().get(chave=chave)


class RelatorioRepository:
    def get_for_update(self, relatorio_id):
        return RelatorioGerado.objects.select_for_update().get(id=relatorio_id, is_active=True)


class ExportacaoRepository:
    def get_for_update(self, exportacao_id):
        return ExportacaoArquivo.objects.select_for_update().get(id=exportacao_id, is_active=True)
