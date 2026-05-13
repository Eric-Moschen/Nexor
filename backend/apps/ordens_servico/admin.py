from django.contrib import admin

from apps.ordens_servico.models import ApontamentoHorasOS, HistoricoOS, ItemServico, MaterialUtilizadoOS, OrdemServico


class ItemServicoInline(admin.TabularInline):
    model = ItemServico
    extra = 0
    readonly_fields = ("valor_total",)


class MaterialUtilizadoInline(admin.TabularInline):
    model = MaterialUtilizadoOS
    extra = 0
    readonly_fields = ("custo_total", "data_utilizacao", "usuario_responsavel")


class ApontamentoHorasInline(admin.TabularInline):
    model = ApontamentoHorasOS
    extra = 0
    readonly_fields = ("total_horas", "custo_total")


class HistoricoOSInline(admin.TabularInline):
    model = HistoricoOS
    extra = 0
    readonly_fields = ("tipo_evento", "descricao", "status_anterior", "status_novo", "usuario_responsavel", "created_at")
    can_delete = False


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ("numero", "cliente", "titulo", "status", "prioridade", "valor_final", "data_abertura")
    list_filter = ("status", "prioridade", "tipo_servico", "data_abertura")
    search_fields = ("numero", "titulo", "descricao_servico", "cliente__razao_social")
    readonly_fields = ("valor_final", "custo_materiais", "custo_mao_obra", "custo_total", "data_abertura", "data_inicio", "data_finalizacao")
    inlines = (ItemServicoInline, MaterialUtilizadoInline, ApontamentoHorasInline, HistoricoOSInline)


@admin.register(HistoricoOS)
class HistoricoOSAdmin(admin.ModelAdmin):
    list_display = ("ordem_servico", "tipo_evento", "status_anterior", "status_novo", "created_at")
    list_filter = ("tipo_evento", "created_at")
    search_fields = ("ordem_servico__numero", "descricao")
