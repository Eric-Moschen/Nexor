from apps.financeiro.models import FinanceiroRecord


def list_records():
    return FinanceiroRecord.objects.filter(is_active=True).order_by("name")
