from django.contrib import admin

from apps.compras.models import (
    HistoricoAprovacaoCompra,
    ItemPedidoCompra,
    ItemSolicitacaoCompra,
    PedidoCompra,
    SolicitacaoCompra,
)


class ItemSolicitacaoCompraInline(admin.TabularInline):
    model = ItemSolicitacaoCompra
    extra = 0


class ItemPedidoCompraInline(admin.TabularInline):
    model = ItemPedidoCompra
    extra = 0


@admin.register(SolicitacaoCompra)
class SolicitacaoCompraAdmin(admin.ModelAdmin):
    list_display = ("numero", "solicitante", "centro_custo", "prioridade", "status", "data_solicitacao")
    list_filter = ("status", "prioridade", "data_solicitacao")
    search_fields = ("numero", "centro_custo", "justificativa")
    inlines = [ItemSolicitacaoCompraInline]


@admin.register(PedidoCompra)
class PedidoCompraAdmin(admin.ModelAdmin):
    list_display = ("numero", "fornecedor", "status", "valor_total", "data_pedido", "previsao_entrega")
    list_filter = ("status", "fornecedor", "data_pedido")
    search_fields = ("numero", "fornecedor__razao_social", "fornecedor__documento")
    inlines = [ItemPedidoCompraInline]


@admin.register(HistoricoAprovacaoCompra)
class HistoricoAprovacaoCompraAdmin(admin.ModelAdmin):
    list_display = ("solicitacao", "acao", "usuario", "status_anterior", "status_posterior", "created_at")
    list_filter = ("acao", "created_at")
    search_fields = ("solicitacao__numero", "motivo")
