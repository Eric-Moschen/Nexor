from apps.clientes.models import Cliente


class ClienteRepository:
    model = Cliente

    def list_active(self):
        return self.model.objects.filter(is_active=True).order_by("razao_social")
from apps.clientes.models import Cliente, InteracaoCRM


class ClienteRepository:
    def get_for_update(self, cliente_id):
        return Cliente.objects.select_for_update().get(id=cliente_id, is_active=True)


class InteracaoCRMRepository:
    def get_for_update(self, interacao_id):
        return InteracaoCRM.objects.select_for_update().get(id=interacao_id, is_active=True)
