from apps.core.audit.services import AuditService
from apps.core.models import AuditLog, Notification
from apps.core.notifications.services import NotificationService


def handle_estoque_baixo(event, event_log):
    AuditService.register(
        user=event.user,
        action=AuditLog.Action.STOCK,
        module="estoque",
        record_model=event.aggregate_type,
        record_id=event.aggregate_id,
        metadata={"event_log": event_log.id, **event.payload},
    )
    NotificationService.notify(
        title="Estoque abaixo do minimo",
        message=event.payload.get("message", "Produto atingiu ponto de reposicao."),
        level=Notification.Level.WARNING,
        category="estoque",
        event=event_log,
        metadata=event.payload,
    )


def handle_material_os_utilizado(event, event_log):
    AuditService.register(
        user=event.user,
        action=AuditLog.Action.STOCK,
        module="ordens_servico",
        record_model=event.aggregate_type,
        record_id=event.aggregate_id,
        metadata={"event_log": event_log.id, **event.payload},
    )
