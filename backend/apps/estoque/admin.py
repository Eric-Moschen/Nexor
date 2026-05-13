from django.contrib import admin

from apps.estoque.models import CategoriaProduto, MovimentacaoEstoque, Produto, UnidadeMedida


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("nome", "descricao")


@admin.register(UnidadeMedida)
class UnidadeMedidaAdmin(admin.ModelAdmin):
    list_display = ("sigla", "nome", "is_active")
    list_filter = ("is_active",)
    search_fields = ("sigla", "nome")


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("codigo_interno", "sku", "nome", "categoria", "estoque_atual", "estoque_minimo", "is_active")
    list_filter = ("is_active", "categoria", "unidade_medida")
    search_fields = ("codigo_interno", "sku", "codigo_barras", "nome")


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ("produto", "tipo", "quantidade", "saldo_anterior", "saldo_posterior", "data_movimentacao")
    list_filter = ("tipo", "data_movimentacao")
    search_fields = ("produto__codigo_interno", "produto__sku", "produto__nome", "observacao")
    readonly_fields = ("produto", "tipo", "quantidade", "saldo_anterior", "saldo_posterior", "usuario_responsavel", "data_movimentacao")
