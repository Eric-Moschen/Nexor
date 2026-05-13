from apps.estoque.models import EstoqueRecord


def create_record(*, name, description="", created_by=None):
    return EstoqueRecord.objects.create(name=name, description=description, created_by=created_by)
