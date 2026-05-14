from django.contrib import admin

from apps.clientes.models import Cliente, ContatoRelacionamento, DocumentoRelacionamento, EnderecoRelacionamento, HistoricoRelacionamento, InteracaoCRM


class EnderecoClienteInline(admin.TabularInline):
    model = EnderecoRelacionamento
    fk_name = "cliente"
    extra = 0


class ContatoClienteInline(admin.TabularInline):
    model = ContatoRelacionamento
    fk_name = "cliente"
    extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "tipo_pessoa", "documento", "status", "email", "telefone", "usuario_responsavel", "is_active")
    list_filter = ("tipo_pessoa", "status", "is_active", "created_at")
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
    inlines = [EnderecoClienteInline, ContatoClienteInline]


@admin.register(InteracaoCRM)
class InteracaoCRMAdmin(admin.ModelAdmin):
    list_display = ("cliente", "tipo_interacao", "responsavel", "status", "data", "proximo_contato")
    list_filter = ("tipo_interacao", "status", "data")
    search_fields = ("cliente__razao_social", "descricao")


@admin.register(HistoricoRelacionamento)
class HistoricoRelacionamentoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "fornecedor", "tipo_evento", "usuario_responsavel", "created_at")
    list_filter = ("tipo_evento", "created_at")
    search_fields = ("cliente__razao_social", "fornecedor__razao_social", "descricao")
    readonly_fields = ("created_at", "updated_at")


@admin.register(DocumentoRelacionamento)
class DocumentoRelacionamentoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_documento", "cliente", "fornecedor", "created_at", "is_active")
    list_filter = ("tipo_documento", "is_active", "created_at")
    search_fields = ("titulo", "cliente__razao_social", "fornecedor__razao_social")
