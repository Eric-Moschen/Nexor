from apps.clientes.models import Cliente


def listar_clientes():
    return Cliente.objects.filter(is_active=True).order_by("razao_social")
