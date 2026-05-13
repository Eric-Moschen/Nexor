from django.contrib import admin

from apps.fiscal.models import ClienteFiscal, EmpresaFiscal, EventoFiscal, FornecedorFiscal, ItemNotaFiscal, NaturezaOperacao, NotaFiscal, ProdutoFiscal


@admin.register(EmpresaFiscal)
class EmpresaFiscalAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "cnpj", "regime_tributario", "ambiente", "is_active")
    list_filter = ("ambiente", "regime_tributario", "is_active")
    search_fields = ("razao_social", "nome_fantasia", "cnpj")
    readonly_fields = ("certificado_senha_protegida", "created_at", "updated_at")


@admin.register(ClienteFiscal)
class ClienteFiscalAdmin(admin.ModelAdmin):
    list_display = ("cliente", "cpf_cnpj", "uf", "indicador_ie", "is_active")
    list_filter = ("uf", "indicador_ie", "is_active")
    search_fields = ("cliente__razao_social", "cpf_cnpj", "email_fiscal")


@admin.register(FornecedorFiscal)
class FornecedorFiscalAdmin(admin.ModelAdmin):
    list_display = ("fornecedor", "cpf_cnpj", "uf", "indicador_ie", "is_active")
    list_filter = ("uf", "indicador_ie", "is_active")
    search_fields = ("fornecedor__razao_social", "cpf_cnpj", "email_fiscal")


@admin.register(ProdutoFiscal)
class ProdutoFiscalAdmin(admin.ModelAdmin):
    list_display = ("produto", "ncm", "cfop_padrao", "cst_csosn", "is_active")
    list_filter = ("origem_mercadoria", "is_active")
    search_fields = ("produto__nome", "ncm", "cfop_padrao")


@admin.register(NaturezaOperacao)
class NaturezaOperacaoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "descricao", "tipo_operacao", "cfop_padrao", "movimenta_estoque", "gera_financeiro", "is_active")
    list_filter = ("tipo_operacao", "movimenta_estoque", "gera_financeiro", "is_active")
    search_fields = ("codigo", "descricao", "cfop_padrao")


class ItemNotaFiscalInline(admin.TabularInline):
    model = ItemNotaFiscal
    extra = 0
    readonly_fields = ("valor_total", "valor_icms", "valor_pis", "valor_cofins", "valor_ipi")


class EventoFiscalInline(admin.TabularInline):
    model = EventoFiscal
    extra = 0
    readonly_fields = ("tipo_evento", "codigo_retorno", "mensagem", "protocolo", "data_evento", "usuario_responsavel")
    can_delete = False


@admin.register(NotaFiscal)
class NotaFiscalAdmin(admin.ModelAdmin):
    list_display = ("numero", "serie", "emitente", "tipo_operacao", "status", "valor_total", "data_emissao")
    list_filter = ("status", "tipo_operacao", "ambiente", "data_emissao")
    search_fields = ("numero", "chave_acesso", "protocolo", "emitente__razao_social")
    readonly_fields = ("chave_acesso", "protocolo", "valor_produtos", "valor_total", "xml_autorizado", "xml_cancelamento", "created_at", "updated_at")
    inlines = (ItemNotaFiscalInline, EventoFiscalInline)


@admin.register(EventoFiscal)
class EventoFiscalAdmin(admin.ModelAdmin):
    list_display = ("nota_fiscal", "tipo_evento", "codigo_retorno", "protocolo", "data_evento")
    list_filter = ("tipo_evento", "data_evento")
    search_fields = ("nota_fiscal__numero", "codigo_retorno", "mensagem", "protocolo")
