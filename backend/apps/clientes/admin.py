from django.contrib import admin

from apps.clientes.models import ClientesRecord


@admin.register(ClientesRecord)
class ClientesRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
