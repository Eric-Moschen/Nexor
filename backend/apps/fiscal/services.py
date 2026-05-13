from apps.fiscal.models import FiscalRecord


def create_record(*, name, description="", created_by=None):
    return FiscalRecord.objects.create(name=name, description=description, created_by=created_by)
