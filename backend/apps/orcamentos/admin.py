from django.contrib import admin

from apps.orcamentos.models import HistoricoOrcamento, ItemProdutoOrcamento, ItemServicoOrcamento, Orcamento


class ItemProdutoOrcamentoInline(admin.TabularInline):
    model = ItemProdutoOrcamento
    extra = 0
    readonly_fields = ("valor_total", "custo_total")


class ItemServicoOrcamentoInline(admin.TabularInline):
    model = ItemServicoOrcamento
    extra = 0
    readonly_fields = ("valor_total",)


class HistoricoOrcamentoInline(admin.TabularInline):
    model = HistoricoOrcamento
    extra = 0
    readonly_fields = ("tipo_evento", "descricao", "status_anterior", "status_novo", "usuario_responsavel", "created_at")
    can_delete = False


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("numero", "cliente", "titulo", "status", "data_validade", "valor_total", "margem_estimada")
    list_filter = ("status", "data_criacao", "data_validade")
    search_fields = ("numero", "titulo", "cliente__razao_social")
    readonly_fields = ("valor_produtos", "valor_servicos", "valor_total", "custo_total", "margem_estimada", "data_criacao", "pdf_gerado")
    inlines = (ItemProdutoOrcamentoInline, ItemServicoOrcamentoInline, HistoricoOrcamentoInline)


@admin.register(HistoricoOrcamento)
class HistoricoOrcamentoAdmin(admin.ModelAdmin):
    list_display = ("orcamento", "tipo_evento", "status_anterior", "status_novo", "created_at")
    list_filter = ("tipo_evento", "created_at")
    search_fields = ("orcamento__numero", "descricao")
