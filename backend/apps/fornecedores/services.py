from apps.fornecedores.models import FornecedoresRecord


def create_record(*, name, description="", created_by=None):
    return FornecedoresRecord.objects.create(name=name, description=description, created_by=created_by)
