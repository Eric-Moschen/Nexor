from apps.core.audit.services import AuditService
from apps.core.models import AuditLog


def handle_conta_paga(event, event_log):
    AuditService.register(
        user=event.user,
        action=AuditLog.Action.FINANCIAL,
        module="financeiro",
        record_model=event.aggregate_type,
        record_id=event.aggregate_id,
        metadata={"event_log": event_log.id, **event.payload},
    )


def handle_conta_recebida(event, event_log):
    handle_conta_paga(event, event_log)
