from django.contrib import admin

from apps.compras.models import ComprasRecord


@admin.register(ComprasRecord)
class ComprasRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
