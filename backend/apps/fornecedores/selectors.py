from apps.clientes.models import HistoricoRelacionamento
from apps.compras.models import PedidoCompra
from apps.financeiro.models import ContaPagar
from apps.fiscal.models import NotaFiscal
from apps.fornecedores.models import Fornecedor


def listar_fornecedores():
    return Fornecedor.objects.prefetch_related("enderecos", "contatos").filter(is_active=True).order_by("razao_social")


def listar_historico_fornecedor(fornecedor_id):
    return HistoricoRelacionamento.objects.select_related("usuario_responsavel").filter(fornecedor_id=fornecedor_id).order_by("-created_at", "-id")


def montar_historico_fornecedor(fornecedor_id):
    eventos = [
        {
            "id": historico.id,
            "tipo_evento": historico.tipo_evento,
            "descricao": historico.descricao,
            "usuario_nome": historico.usuario_responsavel.get_full_name() if historico.usuario_responsavel else "",
            "dados_extras": historico.dados_extras,
            "created_at": historico.created_at,
        }
        for historico in listar_historico_fornecedor(fornecedor_id)
    ]
    eventos.extend(
        {
            "id": f"pedido-compra-{pedido.id}",
            "tipo_evento": "compra",
            "descricao": f"Pedido de compra {pedido.numero} vinculado ao fornecedor com status {pedido.status}.",
            "usuario_nome": "",
            "dados_extras": {"pedido_compra_id": pedido.id, "valor_total": str(pedido.valor_total)},
            "created_at": pedido.created_at,
        }
        for pedido in PedidoCompra.objects.filter(fornecedor_id=fornecedor_id).only("id", "numero", "status", "valor_total", "created_at")
    )
    eventos.extend(
        {
            "id": f"conta-pagar-{conta.id}",
            "tipo_evento": "financeiro",
            "descricao": f"Conta a pagar vinculada ao fornecedor com status {conta.status}.",
            "usuario_nome": "",
            "dados_extras": {"conta_pagar_id": conta.id, "valor_atual": str(conta.valor_atual)},
            "created_at": conta.created_at,
        }
        for conta in ContaPagar.objects.filter(fornecedor_id=fornecedor_id).only("id", "status", "valor_atual", "created_at")
    )
    eventos.extend(
        {
            "id": f"nfe-{nota.id}",
            "tipo_evento": "nfe",
            "descricao": f"NFe {nota.numero}/{nota.serie} vinculada ao fornecedor com status {nota.status}.",
            "usuario_nome": "",
            "dados_extras": {"nota_fiscal_id": nota.id, "valor_total": str(nota.valor_total)},
            "created_at": nota.created_at,
        }
        for nota in NotaFiscal.objects.filter(destinatario_fornecedor_id=fornecedor_id).only("id", "numero", "serie", "status", "valor_total", "created_at")
    )
    return sorted(eventos, key=lambda item: item["created_at"], reverse=True)
