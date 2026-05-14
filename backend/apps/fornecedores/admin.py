from django.contrib import admin

from apps.clientes.models import ContatoRelacionamento, EnderecoRelacionamento
from apps.fornecedores.models import Fornecedor


class EnderecoFornecedorInline(admin.TabularInline):
    model = EnderecoRelacionamento
    fk_name = "fornecedor"
    extra = 0


class ContatoFornecedorInline(admin.TabularInline):
    model = ContatoRelacionamento
    fk_name = "fornecedor"
    extra = 0


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "tipo_pessoa", "documento", "categoria", "status", "email", "telefone", "is_active")
    list_filter = ("tipo_pessoa", "categoria", "status", "is_active", "created_at")
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
    inlines = [EnderecoFornecedorInline, ContatoFornecedorInline]
