from apps.core.models import Notification
from apps.core.notifications.services import NotificationService


def handle_operational_notification(event, event_log):
    NotificationService.notify(
        title=event.payload.get("title", "Fluxo operacional atualizado"),
        message=event.payload.get("message", f"Evento {event.name} processado."),
        level=Notification.Level.INFO,
        category=event.module,
        event=event_log,
        metadata=event.payload,
    )


def handle_critical_notification(event, event_log):
    NotificationService.notify(
        title=event.payload.get("title", "Alerta critico do ERP"),
        message=event.payload.get("message", f"Evento critico {event.name}."),
        level=Notification.Level.CRITICAL,
        category=event.module,
        event=event_log,
        metadata=event.payload,
    )
