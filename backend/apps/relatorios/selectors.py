from apps.relatorios.models import RelatoriosRecord


def list_records():
    return RelatoriosRecord.objects.filter(is_active=True).order_by("name")
