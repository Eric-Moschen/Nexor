from django.contrib import admin

from apps.estoque.models import EstoqueRecord


@admin.register(EstoqueRecord)
class EstoqueRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
