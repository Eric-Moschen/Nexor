from django.contrib import admin

from apps.fiscal.models import FiscalRecord


@admin.register(FiscalRecord)
class FiscalRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
