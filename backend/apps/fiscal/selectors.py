from apps.fiscal.models import FiscalRecord


def list_records():
    return FiscalRecord.objects.filter(is_active=True).order_by("name")
