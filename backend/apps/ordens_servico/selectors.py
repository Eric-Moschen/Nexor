from apps.ordens_servico.models import ApontamentoHorasOS, HistoricoOS, MaterialUtilizadoOS, OrdemServico


def listar_ordens_servico():
    return (
        OrdemServico.objects.select_related(
            "cliente",
            "responsavel_tecnico",
            "usuario_criador",
            "categoria_financeira",
            "centro_custo",
            "conta_receber",
            "nota_fiscal",
        )
        .prefetch_related("itens", "materiais", "apontamentos", "historico")
        .filter(is_active=True)
        .order_by("-data_abertura", "-id")
    )


def listar_materiais_os(ordem_id):
    return MaterialUtilizadoOS.objects.select_related("produto", "usuario_responsavel").filter(ordem_servico_id=ordem_id).order_by("-data_utilizacao", "-id")


def listar_apontamentos_os(ordem_id):
    return ApontamentoHorasOS.objects.select_related("colaborador").filter(ordem_servico_id=ordem_id).order_by("-data", "-hora_inicio", "-id")


def listar_historico_os(ordem_id):
    return HistoricoOS.objects.select_related("usuario_responsavel").filter(ordem_servico_id=ordem_id).order_by("-created_at", "-id")
