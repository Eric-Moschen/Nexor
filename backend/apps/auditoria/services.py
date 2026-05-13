from apps.auditoria.models import AuditoriaRecord


def create_record(*, name, description="", created_by=None):
    return AuditoriaRecord.objects.create(name=name, description=description, created_by=created_by)
