from apps.compras.models import ComprasRecord


def create_record(*, name, description="", created_by=None):
    return ComprasRecord.objects.create(name=name, description=description, created_by=created_by)
