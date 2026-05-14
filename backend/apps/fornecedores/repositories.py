from apps.fornecedores.models import Fornecedor


class FornecedorRepository:
    model = Fornecedor

    def list_active(self):
        return self.model.objects.filter(is_active=True).order_by("razao_social")
from apps.fornecedores.models import Fornecedor


class FornecedorRepository:
    def get_for_update(self, fornecedor_id):
        return Fornecedor.objects.select_for_update().get(id=fornecedor_id, is_active=True)
