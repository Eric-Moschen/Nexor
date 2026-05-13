from apps.auditoria.models import AuditoriaRecord


def list_records():
    return AuditoriaRecord.objects.filter(is_active=True).order_by("name")
