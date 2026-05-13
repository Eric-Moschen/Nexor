from django.db.models import Sum
from django.utils import timezone

from apps.financeiro.enums import StatusContaPagar, StatusContaReceber, TipoBaixa
from apps.financeiro.models import BaixaFinanceira, CategoriaFinanceira, CentroCusto, ContaPagar, ContaReceber


def listar_centros_custo():
    return CentroCusto.objects.filter(is_active=True).order_by("codigo")


def listar_categorias():
    return CategoriaFinanceira.objects.filter(is_active=True).order_by("tipo", "nome")


def listar_contas_pagar():
    return ContaPagar.objects.select_related("fornecedor", "categoria", "centro_custo", "usuario_responsavel").filter(is_active=True)


def listar_contas_receber():
    return ContaReceber.objects.select_related("cliente", "categoria", "centro_custo", "usuario_responsavel").filter(is_active=True)


def fluxo_caixa_resumo():
    total_pago = BaixaFinanceira.objects.filter(tipo=TipoBaixa.PAGAMENTO).aggregate(total=Sum("valor_pago"))["total"] or 0
    total_recebido = BaixaFinanceira.objects.filter(tipo=TipoBaixa.RECEBIMENTO).aggregate(total=Sum("valor_pago"))["total"] or 0
    return {
        "total_pago": total_pago,
        "total_recebido": total_recebido,
        "saldo": total_recebido - total_pago,
    }


def dashboard_financeiro():
    hoje = timezone.localdate()
    total_a_pagar = ContaPagar.objects.filter(status__in=[StatusContaPagar.PENDENTE, StatusContaPagar.PARCIAL], is_active=True).aggregate(total=Sum("valor_atual"))["total"] or 0
    total_a_receber = ContaReceber.objects.filter(status__in=[StatusContaReceber.PENDENTE, StatusContaReceber.PARCIAL], is_active=True).aggregate(total=Sum("valor_atual"))["total"] or 0
    contas_vencidas = ContaPagar.objects.filter(data_vencimento__lt=hoje, status__in=[StatusContaPagar.PENDENTE, StatusContaPagar.PARCIAL], is_active=True).count()
    recebiveis_vencidos = ContaReceber.objects.filter(data_vencimento__lt=hoje, status__in=[StatusContaReceber.PENDENTE, StatusContaReceber.PARCIAL], is_active=True).count()
    return {
        "total_a_pagar": total_a_pagar,
        "total_a_receber": total_a_receber,
        "contas_vencidas": contas_vencidas,
        "recebiveis_vencidos": recebiveis_vencidos,
        "saldo_projetado": total_a_receber - total_a_pagar,
        "fluxo": fluxo_caixa_resumo(),
    }
