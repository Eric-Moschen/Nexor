from apps.clientes.models import Cliente, HistoricoRelacionamento, InteracaoCRM
from apps.financeiro.models import ContaReceber
from apps.fiscal.models import NotaFiscal
from apps.orcamentos.models import Orcamento
from apps.ordens_servico.models import OrdemServico


def listar_clientes():
    return Cliente.objects.prefetch_related("enderecos", "contatos").filter(is_active=True).order_by("razao_social")


def listar_historico_cliente(cliente_id):
    return HistoricoRelacionamento.objects.select_related("usuario_responsavel").filter(cliente_id=cliente_id).order_by("-created_at", "-id")


def montar_historico_cliente(cliente_id):
    eventos = [
        {
            "id": historico.id,
            "tipo_evento": historico.tipo_evento,
            "descricao": historico.descricao,
            "usuario_nome": historico.usuario_responsavel.get_full_name() if historico.usuario_responsavel else "",
            "dados_extras": historico.dados_extras,
            "created_at": historico.created_at,
        }
        for historico in listar_historico_cliente(cliente_id)
    ]
    eventos.extend(
        {
            "id": f"orcamento-{orcamento.id}",
            "tipo_evento": "orcamento",
            "descricao": f"Orcamento {orcamento.numero} vinculado ao cliente com status {orcamento.status}.",
            "usuario_nome": "",
            "dados_extras": {"orcamento_id": orcamento.id, "valor_total": str(orcamento.valor_total)},
            "created_at": orcamento.created_at,
        }
        for orcamento in Orcamento.objects.filter(cliente_id=cliente_id).only("id", "numero", "status", "valor_total", "created_at")
    )
    eventos.extend(
        {
            "id": f"os-{ordem.id}",
            "tipo_evento": "ordem_servico",
            "descricao": f"Ordem de servico {ordem.numero} vinculada ao cliente com status {ordem.status}.",
            "usuario_nome": "",
            "dados_extras": {"ordem_servico_id": ordem.id, "valor_estimado": str(ordem.valor_estimado), "valor_final": str(ordem.valor_final)},
            "created_at": ordem.created_at,
        }
        for ordem in OrdemServico.objects.filter(cliente_id=cliente_id).only("id", "numero", "status", "valor_estimado", "valor_final", "created_at")
    )
    eventos.extend(
        {
            "id": f"conta-receber-{conta.id}",
            "tipo_evento": "financeiro",
            "descricao": f"Conta a receber vinculada ao cliente com status {conta.status}.",
            "usuario_nome": "",
            "dados_extras": {"conta_receber_id": conta.id, "valor_atual": str(conta.valor_atual)},
            "created_at": conta.created_at,
        }
        for conta in ContaReceber.objects.filter(cliente_id=cliente_id).only("id", "status", "valor_atual", "created_at")
    )
    eventos.extend(
        {
            "id": f"nfe-{nota.id}",
            "tipo_evento": "nfe",
            "descricao": f"NFe {nota.numero}/{nota.serie} vinculada ao cliente com status {nota.status}.",
            "usuario_nome": "",
            "dados_extras": {"nota_fiscal_id": nota.id, "valor_total": str(nota.valor_total)},
            "created_at": nota.created_at,
        }
        for nota in NotaFiscal.objects.filter(destinatario_cliente_id=cliente_id).only("id", "numero", "serie", "status", "valor_total", "created_at")
    )
    return sorted(eventos, key=lambda item: item["created_at"], reverse=True)


def listar_interacoes_cliente(cliente_id):
    return InteracaoCRM.objects.select_related("cliente", "responsavel").filter(cliente_id=cliente_id, is_active=True).order_by("-data", "-id")


def listar_interacoes_crm():
    return InteracaoCRM.objects.select_related("cliente", "responsavel").filter(is_active=True).order_by("-data", "-id")
