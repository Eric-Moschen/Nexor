from django.contrib import admin

from apps.core.models import AuditLog, EventLog, Notification


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("module", "action", "record_model", "record_id", "user", "created_at")
    list_filter = ("module", "action", "created_at")
    search_fields = ("record_model", "record_id", "record_repr")
    readonly_fields = ("created_at",)


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    list_display = ("event_name", "module", "aggregate_type", "aggregate_id", "status", "created_at")
    list_filter = ("module", "status", "event_name")
    search_fields = ("event_name", "aggregate_type", "aggregate_id")
    readonly_fields = ("created_at", "processed_at")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "recipient", "is_read", "created_at")
    list_filter = ("category", "level", "is_read")
    search_fields = ("title", "message")
