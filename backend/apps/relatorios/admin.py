from django.contrib import admin

from apps.relatorios.models import DashboardCache, ExportacaoArquivo, RelatorioGerado, RelatoriosRecord


@admin.register(RelatoriosRecord)
class RelatoriosRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")


@admin.register(DashboardCache)
class DashboardCacheAdmin(admin.ModelAdmin):
    list_display = ("chave", "tipo_dashboard", "expires_at", "gerado_por", "updated_at")
    list_filter = ("tipo_dashboard", "expires_at")
    search_fields = ("chave",)


@admin.register(RelatorioGerado)
class RelatorioGeradoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_relatorio", "gerado_por", "created_at", "is_active")
    list_filter = ("tipo_relatorio", "created_at", "is_active")
    search_fields = ("titulo",)


@admin.register(ExportacaoArquivo)
class ExportacaoArquivoAdmin(admin.ModelAdmin):
    list_display = ("tipo_relatorio", "formato", "status", "solicitado_por", "created_at")
    list_filter = ("tipo_relatorio", "formato", "status", "created_at")
    search_fields = ("task_id", "erro")
