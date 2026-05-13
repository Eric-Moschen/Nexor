from django.contrib import admin

from apps.fornecedores.models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "nome_fantasia", "documento", "email", "telefone", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
