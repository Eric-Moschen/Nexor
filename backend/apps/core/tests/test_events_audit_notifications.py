import pytest

from apps.core.audit.services import AuditService
from apps.core.events.base import InternalEvent
from apps.core.events.dispatcher import EventDispatcher
from apps.core.models import AuditLog, EventLog, Notification
from apps.core.notifications.services import NotificationService


@pytest.mark.django_db
def test_event_dispatcher_processa_handler():
    def handler(event, event_log):
        NotificationService.notify(
            title="Evento processado",
            message=event.payload["message"],
            category=event.module,
            event=event_log,
        )

    event_log = EventDispatcher(handlers={"teste_evento": [handler]}).publish(
        InternalEvent(
            name="teste_evento",
            module="core",
            aggregate_type="core.Teste",
            aggregate_id="1",
            payload={"message": "Fluxo integrado"},
        )
    )
    event_log.refresh_from_db()

    assert event_log.status == EventLog.Status.PROCESSED
    assert Notification.objects.filter(event=event_log, title="Evento processado").exists()


@pytest.mark.django_db
def test_event_dispatcher_registra_falha_sem_quebrar_sistema():
    def handler_ok(event, event_log):
        AuditService.register(action=AuditLog.Action.SYSTEM, module=event.module, record_model=event.aggregate_type, record_id=event.aggregate_id)

    def handler_falha(event, event_log):
        raise RuntimeError("falha controlada")

    event_log = EventDispatcher(handlers={"evento_parcial": [handler_ok, handler_falha]}).publish(
        InternalEvent(name="evento_parcial", module="core", aggregate_type="core.Teste", aggregate_id="2")
    )
    event_log.refresh_from_db()

    assert event_log.status == EventLog.Status.PARTIAL
    assert "falha controlada" in event_log.error_message
    assert AuditLog.objects.filter(module="core", record_id="2").exists()


@pytest.mark.django_db
def test_audit_service_registra_log_global():
    log = AuditService.register(action=AuditLog.Action.CREATE, module="auditoria", record_model="core.Teste", record_id="99", after={"ok": True})

    assert log.action == AuditLog.Action.CREATE
    assert log.after == {"ok": True}
