from apps.fiscal.models import NotaFiscal


class NotaFiscalRepository:
    def get_for_update(self, nota_id):
        return NotaFiscal.objects.select_for_update().get(id=nota_id)

    def get_with_relations(self, nota_id):
        return NotaFiscal.objects.select_related("emitente", "natureza_operacao").prefetch_related("itens", "eventos").get(id=nota_id)
