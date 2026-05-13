from apps.estoque.models import EstoqueRecord


def list_records():
    return EstoqueRecord.objects.filter(is_active=True).order_by("name")
