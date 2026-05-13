from apps.fornecedores.models import FornecedoresRecord


def list_records():
    return FornecedoresRecord.objects.filter(is_active=True).order_by("name")
