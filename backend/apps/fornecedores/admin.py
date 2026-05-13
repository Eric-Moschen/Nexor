from django.contrib import admin

from apps.fornecedores.models import FornecedoresRecord


@admin.register(FornecedoresRecord)
class FornecedoresRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
