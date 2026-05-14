from decimal import Decimal

from django.db.models import Count, DecimalField, ExpressionWrapper, F, Sum
from django.db.models.functions import Coalesce, TruncMonth
from django.utils import timezone

from apps.clientes.enums import StatusRelacionamento
from apps.clientes.models import Cliente
from apps.compras.models import PedidoCompra, SolicitacaoCompra
from apps.estoque.models import MovimentacaoEstoque, Produto
from apps.financeiro.enums import StatusContaPagar, StatusContaReceber
from apps.financeiro.models import ContaPagar, ContaReceber
from apps.fiscal.models import NotaFiscal
from apps.fornecedores.models import Fornecedor
from apps.orcamentos.enums import StatusOrcamento
from apps.orcamentos.models import Orcamento
from apps.ordens_servico.enums import StatusOS
from apps.ordens_servico.models import ApontamentoHorasOS, MaterialUtilizadoOS, OrdemServico
from apps.relatorios.models import ExportacaoArquivo, RelatoriosRecord


def list_records():
    return RelatoriosRecord.objects.filter(is_active=True).order_by("name")


def listar_exportacoes(usuario=None):
    queryset = ExportacaoArquivo.objects.select_related("relatorio", "solicitado_por").filter(is_active=True)
    if usuario and not usuario.is_superuser:
        queryset = queryset.filter(solicitado_por=usuario)
    return queryset.order_by("-created_at", "-id")


def _money(value):
    return str(value or Decimal("0.00"))


def _sum(queryset, field):
    return queryset.aggregate(total=Coalesce(Sum(field), Decimal("0.00"), output_field=DecimalField(max_digits=14, decimal_places=2)))["total"]


def _date_filter(queryset, field, filtros, use_date_lookup=True):
    prefix = f"{field}__date" if use_date_lookup else field
    if filtros.get("data_inicial"):
        queryset = queryset.filter(**{f"{prefix}__gte": filtros["data_inicial"]})
    if filtros.get("data_final"):
        queryset = queryset.filter(**{f"{prefix}__lte": filtros["data_final"]})
    return queryset


def _monthly_series(queryset, date_field, value_field):
    rows = []
    for row in queryset.annotate(periodo=TruncMonth(date_field)).values("periodo").annotate(total=Coalesce(Sum(value_field), Decimal("0.00"), output_field=DecimalField(max_digits=14, decimal_places=2))).order_by("periodo"):
        if not row["periodo"]:
            continue
        periodo = row["periodo"].date() if hasattr(row["periodo"], "date") else row["periodo"]
        rows.append({"periodo": periodo.isoformat(), "total": _money(row["total"])})
    return rows


def financeiro_indicadores(filtros=None):
    filtros = filtros or {}
    pagar = _date_filter(ContaPagar.objects.select_related("fornecedor", "categoria", "centro_custo").filter(is_active=True), "data_vencimento", filtros, use_date_lookup=False)
    receber = _date_filter(ContaReceber.objects.select_related("cliente", "categoria", "centro_custo").filter(is_active=True), "data_vencimento", filtros, use_date_lookup=False)
    hoje = timezone.localdate()
    contas_pagar_abertas = pagar.exclude(status__in=[StatusContaPagar.PAGO, StatusContaPagar.CANCELADO])
    contas_receber_abertas = receber.exclude(status__in=[StatusContaReceber.RECEBIDO, StatusContaReceber.CANCELADO])
    total_receita = _sum(receber.filter(status=StatusContaReceber.RECEBIDO), "valor_original")
    total_despesa = _sum(pagar.filter(status=StatusContaPagar.PAGO), "valor_original")
    return {
        "contas_pagar": _money(_sum(contas_pagar_abertas, "valor_atual")),
        "contas_receber": _money(_sum(contas_receber_abertas, "valor_atual")),
        "inadimplencia": _money(_sum(contas_receber_abertas.filter(data_vencimento__lt=hoje), "valor_atual")),
        "receita_mensal": _money(total_receita),
        "despesa_mensal": _money(total_despesa),
        "margem_operacional": _money(total_receita - total_despesa),
        "evolucao_receitas": _monthly_series(receber.filter(status=StatusContaReceber.RECEBIDO), "data_vencimento", "valor_original"),
        "evolucao_despesas": _monthly_series(pagar.filter(status=StatusContaPagar.PAGO), "data_vencimento", "valor_original"),
    }


def estoque_indicadores(filtros=None):
    produtos = Produto.objects.select_related("categoria", "unidade_medida").filter(is_active=True)
    movimentacoes = MovimentacaoEstoque.objects.select_related("produto").filter(produto__is_active=True)
    if filtros and filtros.get("data_inicial"):
        movimentacoes = movimentacoes.filter(data_movimentacao__date__gte=filtros["data_inicial"])
    if filtros and filtros.get("data_final"):
        movimentacoes = movimentacoes.filter(data_movimentacao__date__lte=filtros["data_final"])
    baixo_estoque = produtos.filter(estoque_atual__lte=F("estoque_minimo"))
    custo_expr = ExpressionWrapper(F("estoque_atual") * F("custo_medio"), output_field=DecimalField(max_digits=14, decimal_places=2))
    custo_estoque = produtos.aggregate(total=Coalesce(Sum(custo_expr), Decimal("0.00"), output_field=DecimalField(max_digits=14, decimal_places=2)))["total"]
    mais_movimentados = list(
        movimentacoes.values("produto_id", "produto__nome")
        .annotate(total=Coalesce(Sum("quantidade"), Decimal("0.0000"), output_field=DecimalField(max_digits=14, decimal_places=4)))
        .order_by("-total")[:10]
    )
    return {
        "produtos_sem_estoque": produtos.filter(estoque_atual=0).count(),
        "produtos_abaixo_minimo": baixo_estoque.count(),
        "custo_estoque": _money(custo_estoque),
        "entradas": _money(_sum(movimentacoes.filter(tipo=MovimentacaoEstoque.Tipo.ENTRADA), "quantidade")),
        "saidas": _money(_sum(movimentacoes.filter(tipo=MovimentacaoEstoque.Tipo.SAIDA), "quantidade")),
        "produtos_criticos": [
            {
                "id": produto.id,
                "codigo_interno": produto.codigo_interno,
                "nome": produto.nome,
                "estoque_atual": str(produto.estoque_atual),
                "estoque_minimo": str(produto.estoque_minimo),
            }
            for produto in baixo_estoque.only("id", "codigo_interno", "nome", "estoque_atual", "estoque_minimo")[:10]
        ],
        "produtos_mais_movimentados": [{"produto": row["produto__nome"], "quantidade": str(row["total"])} for row in mais_movimentados],
    }


def comercial_indicadores(filtros=None):
    filtros = filtros or {}
    orcamentos = _date_filter(Orcamento.objects.select_related("cliente").filter(is_active=True), "created_at", filtros)
    clientes = Cliente.objects.filter(is_active=True)
    enviados = orcamentos.filter(status__in=[StatusOrcamento.ENVIADO, StatusOrcamento.APROVADO, StatusOrcamento.REPROVADO, StatusOrcamento.CONVERTIDO_OS])
    aprovados = orcamentos.filter(status__in=[StatusOrcamento.APROVADO, StatusOrcamento.CONVERTIDO_OS])
    faturadas = OrdemServico.objects.filter(status=StatusOS.FATURADA, is_active=True)
    total_faturado = _sum(faturadas, "valor_final")
    receita_por_cliente = (
        ContaReceber.objects.select_related("cliente")
        .filter(status=StatusContaReceber.RECEBIDO, is_active=True)
        .values("cliente_id", "cliente__razao_social")
        .annotate(total=Coalesce(Sum("valor_original"), Decimal("0.00"), output_field=DecimalField(max_digits=14, decimal_places=2)))
        .order_by("-total")[:10]
    )
    return {
        "orcamentos_enviados": enviados.count(),
        "taxa_aprovacao": round((aprovados.count() / enviados.count()) * 100, 2) if enviados.exists() else 0,
        "taxa_conversao": round((orcamentos.filter(status=StatusOrcamento.CONVERTIDO_OS).count() / enviados.count()) * 100, 2) if enviados.exists() else 0,
        "clientes_ativos": clientes.filter(status=StatusRelacionamento.ATIVO).count(),
        "clientes_inativos": clientes.filter(status=StatusRelacionamento.INATIVO).count(),
        "ticket_medio": _money(total_faturado / faturadas.count() if faturadas.exists() else Decimal("0.00")),
        "os_faturadas": faturadas.count(),
        "receita_por_cliente": [{"cliente": row["cliente__razao_social"], "total": _money(row["total"])} for row in receita_por_cliente],
    }


def operacional_indicadores(filtros=None):
    filtros = filtros or {}
    ordens = _date_filter(OrdemServico.objects.select_related("cliente", "responsavel_tecnico").filter(is_active=True), "data_abertura", filtros)
    hoje = timezone.localdate()
    apontamentos = ApontamentoHorasOS.objects.select_related("ordem_servico", "colaborador").filter(ordem_servico__is_active=True)
    materiais = MaterialUtilizadoOS.objects.select_related("ordem_servico", "produto").filter(ordem_servico__is_active=True)
    horas_por_colaborador = apontamentos.values("colaborador_id", "colaborador__username").annotate(total=Coalesce(Sum("total_horas"), Decimal("0.00"), output_field=DecimalField(max_digits=14, decimal_places=2))).order_by("-total")[:10]
    servicos = ordens.values("tipo_servico").annotate(total=Count("id")).order_by("-total")[:10]
    return {
        "os_em_execucao": ordens.filter(status=StatusOS.EM_EXECUCAO).count(),
        "os_atrasadas": ordens.exclude(status__in=[StatusOS.FINALIZADA, StatusOS.FATURADA, StatusOS.CANCELADA]).filter(data_prevista__lt=hoje).count(),
        "horas_apontadas": _money(_sum(apontamentos, "total_horas")),
        "produtividade": [{"colaborador": row["colaborador__username"], "horas": _money(row["total"])} for row in horas_por_colaborador],
        "custos_operacionais": _money(_sum(ordens, "custo_total")),
        "servicos_mais_executados": [{"servico": row["tipo_servico"], "total": row["total"]} for row in servicos],
        "materiais_utilizados": _money(_sum(materiais, "custo_total")),
    }


def executivo_indicadores(filtros=None):
    financeiro = financeiro_indicadores(filtros)
    estoque = estoque_indicadores(filtros)
    comercial = comercial_indicadores(filtros)
    operacional = operacional_indicadores(filtros)
    compras_pendentes = PedidoCompra.objects.filter(is_active=True).exclude(status__in=[PedidoCompra.Status.RECEBIDO, PedidoCompra.Status.CANCELADO]).count()
    return {
        "total_faturado": _money(_sum(NotaFiscal.objects.filter(is_active=True), "valor_total")),
        "total_recebido": financeiro["receita_mensal"],
        "total_em_aberto": financeiro["contas_receber"],
        "total_os_abertas": OrdemServico.objects.filter(is_active=True).exclude(status__in=[StatusOS.FINALIZADA, StatusOS.FATURADA, StatusOS.CANCELADA]).count(),
        "total_orcamentos_pendentes": Orcamento.objects.filter(is_active=True, status__in=[StatusOrcamento.RASCUNHO, StatusOrcamento.EM_ANALISE, StatusOrcamento.ENVIADO]).count(),
        "total_compras_pendentes": compras_pendentes,
        "produtos_baixo_estoque": estoque["produtos_abaixo_minimo"],
        "fluxo_financeiro": financeiro,
        "indicadores_mensais": {
            "financeiro": financeiro["evolucao_receitas"],
            "despesas": financeiro["evolucao_despesas"],
        },
        "operacional": operacional,
        "comercial": comercial,
    }


def relatorio_financeiro(filtros=None):
    indicadores = financeiro_indicadores(filtros)
    contas_vencidas = ContaReceber.objects.select_related("cliente").filter(is_active=True, status=StatusContaReceber.VENCIDO).values("id", "cliente__razao_social", "descricao", "valor_atual", "data_vencimento")[:50]
    return {"indicadores": indicadores, "contas_vencidas": list(contas_vencidas)}


def relatorio_estoque(filtros=None):
    indicadores = estoque_indicadores(filtros)
    inventario = Produto.objects.select_related("categoria").filter(is_active=True).values("id", "codigo_interno", "nome", "estoque_atual", "estoque_minimo", "custo_medio")[:100]
    return {"indicadores": indicadores, "inventario": list(inventario)}


def relatorio_comercial(filtros=None):
    return {"indicadores": comercial_indicadores(filtros), "orcamentos": list(Orcamento.objects.select_related("cliente").filter(is_active=True).values("id", "numero", "cliente__razao_social", "status", "valor_total", "created_at")[:100])}


def relatorio_os(filtros=None):
    return {"indicadores": operacional_indicadores(filtros), "ordens": list(OrdemServico.objects.select_related("cliente").filter(is_active=True).values("id", "numero", "cliente__razao_social", "status", "valor_estimado", "valor_final", "created_at")[:100])}


def relatorio_compras(filtros=None):
    pedidos = PedidoCompra.objects.select_related("fornecedor").filter(is_active=True)
    solicitacoes_pendentes = SolicitacaoCompra.objects.filter(is_active=True, status=SolicitacaoCompra.Status.PENDENTE).count()
    compras_por_fornecedor = pedidos.values("fornecedor_id", "fornecedor__razao_social").annotate(total=Coalesce(Sum("valor_total"), Decimal("0.00"), output_field=DecimalField(max_digits=14, decimal_places=2))).order_by("-total")[:10]
    return {
        "indicadores": {
            "pedidos_pendentes": pedidos.exclude(status__in=[PedidoCompra.Status.RECEBIDO, PedidoCompra.Status.CANCELADO]).count(),
            "solicitacoes_pendentes": solicitacoes_pendentes,
            "total_compras": _money(_sum(pedidos, "valor_total")),
            "compras_por_fornecedor": [{"fornecedor": row["fornecedor__razao_social"], "total": _money(row["total"])} for row in compras_por_fornecedor],
        },
        "pedidos": list(pedidos.values("id", "numero", "fornecedor__razao_social", "status", "valor_total", "data_pedido")[:100]),
    }
