from django.contrib import admin

from apps.financeiro.models import BaixaFinanceira, CategoriaFinanceira, CentroCusto, ContaPagar, ContaReceber, Parcelamento


@admin.register(CentroCusto)
class CentroCustoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "is_active")
    search_fields = ("codigo", "nome")
    list_filter = ("is_active",)


@admin.register(CategoriaFinanceira)
class CategoriaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "is_active")
    search_fields = ("nome",)
    list_filter = ("tipo", "is_active")


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ("numero_lancamento", "fornecedor", "valor_original", "valor_atual", "data_vencimento", "status")
    search_fields = ("numero_lancamento", "fornecedor__razao_social", "descricao")
    list_filter = ("status", "data_vencimento", "centro_custo")


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ("numero_lancamento", "cliente", "valor_original", "valor_atual", "data_vencimento", "status")
    search_fields = ("numero_lancamento", "cliente__razao_social", "descricao")
    list_filter = ("status", "data_vencimento", "centro_custo")


@admin.register(BaixaFinanceira)
class BaixaFinanceiraAdmin(admin.ModelAdmin):
    list_display = ("tipo", "valor_pago", "data_pagamento", "usuario_responsavel")
    list_filter = ("tipo", "data_pagamento")


@admin.register(Parcelamento)
class ParcelamentoAdmin(admin.ModelAdmin):
    list_display = ("descricao", "quantidade_parcelas", "valor_total", "data_primeiro_vencimento")
