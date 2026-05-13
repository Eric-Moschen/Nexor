from django.contrib import admin

from apps.clientes.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "nome_fantasia", "documento", "email", "telefone", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("razao_social", "nome_fantasia", "documento", "email")
