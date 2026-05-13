from apps.compras.models import PedidoCompra, SolicitacaoCompra


def listar_solicitacoes():
    return (
        SolicitacaoCompra.objects.select_related("solicitante", "aprovador")
        .prefetch_related("itens", "itens__produto", "itens__unidade_medida")
        .filter(is_active=True)
        .order_by("-data_solicitacao", "-id")
    )


def listar_pedidos():
    return (
        PedidoCompra.objects.select_related("fornecedor", "solicitacao_origem")
        .prefetch_related("itens", "itens__produto", "itens__unidade_medida")
        .filter(is_active=True)
        .order_by("-data_pedido", "-id")
    )
