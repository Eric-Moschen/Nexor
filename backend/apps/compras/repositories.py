from apps.compras.models import PedidoCompra, SolicitacaoCompra


class SolicitacaoCompraRepository:
    model = SolicitacaoCompra

    def get_for_update(self, solicitacao_id):
        return self.model.objects.select_for_update().prefetch_related("itens").get(id=solicitacao_id, is_active=True)


class PedidoCompraRepository:
    model = PedidoCompra

    def get_for_update(self, pedido_id):
        return self.model.objects.select_for_update().prefetch_related("itens").get(id=pedido_id, is_active=True)
