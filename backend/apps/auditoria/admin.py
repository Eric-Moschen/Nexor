from django.contrib import admin

from apps.auditoria.models import AuditoriaRecord


@admin.register(AuditoriaRecord)
class AuditoriaRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
