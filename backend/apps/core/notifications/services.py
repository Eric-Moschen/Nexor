from django.utils import timezone

from apps.core.models import Notification


class NotificationService:
    @staticmethod
    def notify(*, title, message, recipient=None, level=Notification.Level.INFO, category="sistema", event=None, metadata=None):
        return Notification.objects.create(
            recipient=recipient if getattr(recipient, "is_authenticated", False) else recipient,
            title=title,
            message=message,
            level=level,
            category=category,
            event=event,
            metadata=metadata or {},
        )

    @staticmethod
    def notify_users(*, users, title, message, level=Notification.Level.INFO, category="sistema", event=None, metadata=None):
        return [
            NotificationService.notify(
                title=title,
                message=message,
                recipient=user,
                level=level,
                category=category,
                event=event,
                metadata=metadata,
            )
            for user in users
        ]

    @staticmethod
    def mark_read(notification, *, user):
        if notification.recipient_id and notification.recipient_id != user.id:
            raise PermissionError("Notificacao pertence a outro usuario.")
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=["is_read", "read_at"])
        return notification

    @staticmethod
    def prepare_email(notification):
        return {"subject": notification.title, "body": notification.message, "metadata": notification.metadata}

    @staticmethod
    def prepare_whatsapp(notification):
        return {"message": f"{notification.title}: {notification.message}", "metadata": notification.metadata}
