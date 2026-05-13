from apps.orcamentos.models import Orcamento


class OrcamentoRepository:
    def get_for_update(self, orcamento_id):
        return Orcamento.objects.select_for_update().get(id=orcamento_id, is_active=True)

    def get_active(self, orcamento_id):
        return Orcamento.objects.get(id=orcamento_id, is_active=True)
