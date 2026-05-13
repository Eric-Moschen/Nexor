from django.contrib import admin

from apps.relatorios.models import RelatoriosRecord


@admin.register(RelatoriosRecord)
class RelatoriosRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
