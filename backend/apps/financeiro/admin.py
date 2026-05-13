from django.contrib import admin

from apps.financeiro.models import FinanceiroRecord


@admin.register(FinanceiroRecord)
class FinanceiroRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
