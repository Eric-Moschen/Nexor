from apps.fornecedores.models import Fornecedor


class FornecedorRepository:
    model = Fornecedor

    def list_active(self):
        return self.model.objects.filter(is_active=True).order_by("razao_social")
