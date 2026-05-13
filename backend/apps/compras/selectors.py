from apps.compras.models import ComprasRecord


def list_records():
    return ComprasRecord.objects.filter(is_active=True).order_by("name")
