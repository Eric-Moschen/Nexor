from apps.clientes.models import Cliente


class ClienteRepository:
    model = Cliente

    def list_active(self):
        return self.model.objects.filter(is_active=True).order_by("razao_social")
