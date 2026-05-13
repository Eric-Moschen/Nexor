from apps.orcamentos.models import HistoricoOrcamento, Orcamento


def listar_orcamentos():
    return (
        Orcamento.objects.select_related("cliente", "usuario_responsavel", "ordem_servico")
        .prefetch_related("itens_produto", "itens_produto__produto", "itens_servico", "historico")
        .filter(is_active=True)
        .order_by("-data_criacao", "-id")
    )


def listar_historico_orcamento(orcamento_id):
    return HistoricoOrcamento.objects.select_related("usuario_responsavel").filter(orcamento_id=orcamento_id).order_by("-created_at", "-id")
