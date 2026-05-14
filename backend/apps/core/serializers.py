from rest_framework import serializers

from apps.core.models import AuditLog, EventLog, Notification


class AuditLogSerializer(serializers.ModelSerializer):
    user_display = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "user",
            "user_display",
            "action",
            "module",
            "record_model",
            "record_id",
            "record_repr",
            "before",
            "after",
            "metadata",
            "ip_address",
            "created_at",
        )
        read_only_fields = fields


class EventLogSerializer(serializers.ModelSerializer):
    user_display = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = EventLog
        fields = (
            "id",
            "event_name",
            "module",
            "aggregate_type",
            "aggregate_id",
            "payload",
            "status",
            "handlers_processed",
            "error_message",
            "user",
            "user_display",
            "ip_address",
            "created_at",
            "processed_at",
        )
        read_only_fields = fields


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "recipient",
            "title",
            "message",
            "level",
            "category",
            "event",
            "metadata",
            "is_read",
            "read_at",
            "created_at",
        )
        read_only_fields = fields
