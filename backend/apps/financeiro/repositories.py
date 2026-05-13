from apps.financeiro.models import ContaPagar, ContaReceber


class ContaPagarRepository:
    model = ContaPagar

    def get_for_update(self, conta_id):
        return self.model.objects.select_for_update().get(id=conta_id, is_active=True)


class ContaReceberRepository:
    model = ContaReceber

    def get_for_update(self, conta_id):
        return self.model.objects.select_for_update().get(id=conta_id, is_active=True)
