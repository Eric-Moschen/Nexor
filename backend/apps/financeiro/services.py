from apps.financeiro.models import FinanceiroRecord


def create_record(*, name, description="", created_by=None):
    return FinanceiroRecord.objects.create(name=name, description=description, created_by=created_by)
