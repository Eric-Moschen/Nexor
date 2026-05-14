from django.db import transaction

from apps.core.events.base import InternalEvent
from apps.core.models import EventLog


class EventDispatcher:
    def __init__(self, handlers=None):
        self.handlers = handlers if handlers is not None else self._default_handlers()

    def publish(self, event: InternalEvent):
        event_log = EventLog.objects.create(
            event_name=event.name,
            module=event.module,
            aggregate_type=event.aggregate_type,
            aggregate_id=str(event.aggregate_id or ""),
            payload=event.payload,
            user=event.user if getattr(event.user, "is_authenticated", False) else None,
            ip_address=event.ip_address,
        )

        def process():
            processed = []
            errors = []
            for handler in self.handlers.get(event.name, []):
                try:
                    handler(event, event_log)
                    processed.append(f"{handler.__module__}.{handler.__name__}")
                except Exception as exc:
                    errors.append(f"{handler.__module__}.{handler.__name__}: {exc}")
            if errors:
                event_log.mark_partial(processed, " | ".join(errors))
            else:
                event_log.mark_processed(processed)

        transaction.on_commit(process)
        return event_log

    def _default_handlers(self):
        from apps.core.events.handlers.financeiro_handlers import handle_conta_paga, handle_conta_recebida
        from apps.core.events.handlers.fiscal_handlers import handle_nfe_autorizada, handle_nfe_rejeitada
        from apps.core.events.handlers.notificacoes_handlers import handle_critical_notification, handle_operational_notification
        from apps.core.events.handlers.estoque_handlers import handle_estoque_baixo, handle_material_os_utilizado
        from apps.core.events.base import (
            CONTA_PAGA,
            CONTA_RECEBIDA,
            ESTOQUE_BAIXO,
            MATERIAL_OS_UTILIZADO,
            NFE_AUTORIZADA,
            NFE_REJEITADA,
            ORCAMENTO_APROVADO,
            OS_FATURADA,
            OS_FINALIZADA,
            PEDIDO_RECEBIDO,
        )

        return {
            ORCAMENTO_APROVADO: [handle_operational_notification],
            OS_FINALIZADA: [handle_operational_notification],
            OS_FATURADA: [handle_operational_notification],
            PEDIDO_RECEBIDO: [handle_operational_notification],
            NFE_AUTORIZADA: [handle_nfe_autorizada, handle_operational_notification],
            NFE_REJEITADA: [handle_nfe_rejeitada, handle_critical_notification],
            CONTA_PAGA: [handle_conta_paga],
            CONTA_RECEBIDA: [handle_conta_recebida],
            ESTOQUE_BAIXO: [handle_estoque_baixo, handle_critical_notification],
            MATERIAL_OS_UTILIZADO: [handle_material_os_utilizado],
        }
