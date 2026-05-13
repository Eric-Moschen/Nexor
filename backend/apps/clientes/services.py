from apps.clientes.models import ClientesRecord


def create_record(*, name, description="", created_by=None):
    return ClientesRecord.objects.create(name=name, description=description, created_by=created_by)
