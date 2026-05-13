from django.contrib import admin

from apps.ordens_servico.models import OrdensServicoRecord


@admin.register(OrdensServicoRecord)
class OrdensServicoRecordAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
