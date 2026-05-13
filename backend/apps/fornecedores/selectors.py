from apps.fornecedores.models import Fornecedor


def listar_fornecedores():
    return Fornecedor.objects.filter(is_active=True).order_by("razao_social")
