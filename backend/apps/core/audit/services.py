from django.forms.models import model_to_dict

from apps.core.models import AuditLog


class AuditService:
    @staticmethod
    def register(*, user=None, action=AuditLog.Action.SYSTEM, module, record=None, record_model="", record_id="", record_repr="", before=None, after=None, ip_address=None, metadata=None):
        if record is not None:
            record_model = record_model or f"{record._meta.app_label}.{record._meta.model_name}"
            record_id = record_id or str(record.pk or "")
            record_repr = record_repr or str(record)[:220]
        return AuditLog.objects.create(
            user=user if getattr(user, "is_authenticated", False) else None,
            action=action,
            module=module,
            record_model=record_model,
            record_id=record_id,
            record_repr=record_repr,
            before=before or {},
            after=after or {},
            ip_address=ip_address,
            metadata=metadata or {},
        )

    @staticmethod
    def register_change(*, user=None, module, record, before=None, after=None, ip_address=None, metadata=None):
        previous = before if before is not None else {}
        current = after if after is not None else model_to_dict(record)
        return AuditService.register(
            user=user,
            action=AuditLog.Action.UPDATE,
            module=module,
            record=record,
            before=previous,
            after=current,
            ip_address=ip_address,
            metadata=metadata,
        )

    @staticmethod
    def register_critical_event(*, event_name, module, user=None, record=None, ip_address=None, metadata=None):
        return AuditService.register(
            user=user,
            action=AuditLog.Action.SYSTEM,
            module=module,
            record=record,
            record_model=event_name if record is None else "",
            before={},
            after={},
            ip_address=ip_address,
            metadata=metadata or {},
        )
