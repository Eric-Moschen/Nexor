from apps.clientes.models import ClientesRecord


def list_records():
    return ClientesRecord.objects.filter(is_active=True).order_by("name")
