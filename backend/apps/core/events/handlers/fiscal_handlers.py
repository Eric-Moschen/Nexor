from apps.core.audit.services import AuditService
from apps.core.models import AuditLog, Notification
from apps.core.notifications.services import NotificationService


def handle_nfe_autorizada(event, event_log):
    AuditService.register(
        user=event.user,
        action=AuditLog.Action.FISCAL,
        module="fiscal",
        record_model=event.aggregate_type,
        record_id=event.aggregate_id,
        metadata={"event_log": event_log.id, **event.payload},
    )


def handle_nfe_rejeitada(event, event_log):
    AuditService.register(
        user=event.user,
        action=AuditLog.Action.FISCAL,
        module="fiscal",
        record_model=event.aggregate_type,
        record_id=event.aggregate_id,
        metadata={"event_log": event_log.id, **event.payload},
    )
    NotificationService.notify(
        title="NFe rejeitada",
        message=event.payload.get("message", "A emissao fiscal retornou rejeicao."),
        level=Notification.Level.CRITICAL,
        category="fiscal",
        event=event_log,
        metadata=event.payload,
    )
