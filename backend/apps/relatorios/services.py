from apps.relatorios.models import RelatoriosRecord


def create_record(*, name, description="", created_by=None):
    return RelatoriosRecord.objects.create(name=name, description=description, created_by=created_by)
