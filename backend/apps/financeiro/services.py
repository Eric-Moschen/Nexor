from calendar import monthrange
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.compras.models import PedidoCompra
from apps.financeiro.enums import StatusContaPagar, StatusContaReceber, TipoBaixa, TipoFinanceiro
from apps.financeiro.models import BaixaFinanceira, ContaPagar, ContaReceber, Parcelamento
from apps.financeiro.repositories import ContaPagarRepository, ContaReceberRepository


class FinanceiroService:
    def __init__(self, conta_pagar_repository=None, conta_receber_repository=None):
        self.conta_pagar_repository = conta_pagar_repository or ContaPagarRepository()
        self.conta_receber_repository = conta_receber_repository or ContaReceberRepository()

    @transaction.atomic
    def criar_conta_pagar(self, *, usuario, **dados):
        self._validar_conta(dados)
        if dados["categoria"].tipo != TipoFinanceiro.DESPESA:
            raise ValidationError("Conta a pagar exige categoria de despesa.")
        valor = Decimal(str(dados["valor_original"]))
        conta = ContaPagar.objects.create(
            numero_lancamento=self._proximo_numero("CP", ContaPagar),
            valor_atual=valor,
            usuario_responsavel=usuario,
            created_by=usuario,
            updated_by=usuario,
            **dados,
        )
        self.atualizar_status_conta_pagar(conta)
        return conta

    @transaction.atomic
    def criar_conta_receber(self, *, usuario, **dados):
        self._validar_conta(dados)
        if dados["categoria"].tipo != TipoFinanceiro.RECEITA:
            raise ValidationError("Conta a receber exige categoria de receita.")
        valor = Decimal(str(dados["valor_original"]))
        conta = ContaReceber.objects.create(
            numero_lancamento=self._proximo_numero("CR", ContaReceber),
            valor_atual=valor,
            usuario_responsavel=usuario,
            created_by=usuario,
            updated_by=usuario,
            **dados,
        )
        self.atualizar_status_conta_receber(conta)
        return conta

    @transaction.atomic
    def baixar_conta_pagar(self, *, conta_id, usuario, **dados):
        conta = self.conta_pagar_repository.get_for_update(conta_id)
        self._validar_baixa(conta, dados)
        baixa = BaixaFinanceira.objects.create(
            conta_pagar=conta,
            tipo=TipoBaixa.PAGAMENTO,
            usuario_responsavel=usuario,
            **dados,
        )
        conta.valor_atual = self._saldo_apos_baixa(conta, baixa)
        self.atualizar_status_conta_pagar(conta)
        if conta.valor_atual <= 0:
            from apps.core.events.base import CONTA_PAGA, InternalEvent
            from apps.core.events.dispatcher import EventDispatcher

            EventDispatcher().publish(InternalEvent(
                name=CONTA_PAGA,
                module="financeiro",
                aggregate_type="financeiro.ContaPagar",
                aggregate_id=str(conta.id),
                payload={"title": "Conta paga", "message": f"Conta a pagar {conta.numero_lancamento} quitada.", "baixa": baixa.id},
                user=usuario,
            ))
        return baixa

    @transaction.atomic
    def baixar_conta_receber(self, *, conta_id, usuario, **dados):
        conta = self.conta_receber_repository.get_for_update(conta_id)
        self._validar_baixa(conta, dados)
        baixa = BaixaFinanceira.objects.create(
            conta_receber=conta,
            tipo=TipoBaixa.RECEBIMENTO,
            usuario_responsavel=usuario,
            **dados,
        )
        conta.valor_atual = self._saldo_apos_baixa(conta, baixa)
        self.atualizar_status_conta_receber(conta)
        if conta.valor_atual <= 0:
            from apps.core.events.base import CONTA_RECEBIDA, InternalEvent
            from apps.core.events.dispatcher import EventDispatcher

            EventDispatcher().publish(InternalEvent(
                name=CONTA_RECEBIDA,
                module="financeiro",
                aggregate_type="financeiro.ContaReceber",
                aggregate_id=str(conta.id),
                payload={"title": "Conta recebida", "message": f"Conta a receber {conta.numero_lancamento} quitada.", "baixa": baixa.id},
                user=usuario,
            ))
        return baixa

    @transaction.atomic
    def cancelar_conta_pagar(self, *, conta_id, usuario):
        conta = self.conta_pagar_repository.get_for_update(conta_id)
        if conta.status == StatusContaPagar.PAGO:
            raise ValidationError("Conta paga nao pode ser cancelada sem regra de estorno.")
        conta.status = StatusContaPagar.CANCELADO
        conta.updated_by = usuario
        conta.save(update_fields=["status", "updated_by", "updated_at"])
        return conta

    @transaction.atomic
    def cancelar_conta_receber(self, *, conta_id, usuario):
        conta = self.conta_receber_repository.get_for_update(conta_id)
        if conta.status == StatusContaReceber.RECEBIDO:
            raise ValidationError("Conta recebida nao pode ser cancelada sem regra de estorno.")
        conta.status = StatusContaReceber.CANCELADO
        conta.updated_by = usuario
        conta.save(update_fields=["status", "updated_by", "updated_at"])
        return conta

    @transaction.atomic
    def gerar_conta_pagar_de_pedido(self, *, pedido_id, categoria, centro_custo, data_vencimento, usuario):
        pedido = PedidoCompra.objects.get(id=pedido_id)
        if pedido.valor_total <= 0:
            raise ValidationError("Pedido sem valor total nao gera conta a pagar.")
        if ContaPagar.objects.filter(pedido_compra_origem=pedido, is_active=True).exists():
            raise ValidationError("Pedido ja possui conta a pagar ativa.")
        return self.criar_conta_pagar(
            usuario=usuario,
            fornecedor=pedido.fornecedor,
            descricao=f"Pedido de compra {pedido.numero}",
            categoria=categoria,
            centro_custo=centro_custo,
            valor_original=pedido.valor_total,
            data_emissao=timezone.localdate(),
            data_vencimento=data_vencimento,
            pedido_compra_origem=pedido,
        )

    def gerar_parcelamento(self, *, descricao, valor_total, quantidade_parcelas, data_primeiro_vencimento, intervalo_meses=1, usuario=None):
        if quantidade_parcelas <= 0:
            raise ValidationError("Quantidade de parcelas invalida.")
        parcelamento = Parcelamento.objects.create(
            descricao=descricao,
            valor_total=valor_total,
            quantidade_parcelas=quantidade_parcelas,
            data_primeiro_vencimento=data_primeiro_vencimento,
            intervalo_meses=intervalo_meses,
            created_by=usuario,
            updated_by=usuario,
        )
        valor_parcela = Decimal(str(valor_total)) / Decimal(str(quantidade_parcelas))
        vencimentos = [self._somar_meses(data_primeiro_vencimento, intervalo_meses * index) for index in range(quantidade_parcelas)]
        return parcelamento, valor_parcela, vencimentos

    def atualizar_status_conta_pagar(self, conta):
        if conta.status == StatusContaPagar.CANCELADO:
            return conta
        if conta.valor_atual <= 0:
            conta.status = StatusContaPagar.PAGO
        elif conta.valor_atual < conta.valor_original:
            conta.status = StatusContaPagar.PARCIAL
        elif conta.data_vencimento < timezone.localdate():
            conta.status = StatusContaPagar.VENCIDO
        else:
            conta.status = StatusContaPagar.PENDENTE
        conta.save(update_fields=["valor_atual", "status", "updated_at"])
        return conta

    def atualizar_status_conta_receber(self, conta):
        if conta.status == StatusContaReceber.CANCELADO:
            return conta
        if conta.valor_atual <= 0:
            conta.status = StatusContaReceber.RECEBIDO
        elif conta.valor_atual < conta.valor_original:
            conta.status = StatusContaReceber.PARCIAL
        elif conta.data_vencimento < timezone.localdate():
            conta.status = StatusContaReceber.VENCIDO
        else:
            conta.status = StatusContaReceber.PENDENTE
        conta.save(update_fields=["valor_atual", "status", "updated_at"])
        return conta

    def _validar_conta(self, dados):
        if not dados.get("categoria"):
            raise ValidationError("Categoria financeira obrigatoria.")
        if not dados.get("centro_custo"):
            raise ValidationError("Centro de custo obrigatorio.")
        if Decimal(str(dados.get("valor_original", 0))) <= 0:
            raise ValidationError("Valor original deve ser maior que zero.")
        if dados["data_vencimento"] < dados["data_emissao"]:
            raise ValidationError("Data de vencimento nao pode ser anterior a emissao.")

    def _validar_baixa(self, conta, dados):
        if conta.status in {StatusContaPagar.CANCELADO, StatusContaPagar.PAGO, StatusContaReceber.CANCELADO, StatusContaReceber.RECEBIDO}:
            raise ValidationError("Conta nao permite baixa neste status.")
        valor_liquido = Decimal(str(dados["valor_pago"])) + Decimal(str(dados.get("multa", 0))) + Decimal(str(dados.get("juros", 0))) - Decimal(str(dados.get("desconto", 0)))
        if valor_liquido <= 0:
            raise ValidationError("Valor liquido da baixa deve ser maior que zero.")
        if valor_liquido > conta.valor_atual:
            raise ValidationError("Valor da baixa excede saldo pendente.")

    def _saldo_apos_baixa(self, conta, baixa):
        saldo = conta.valor_atual - baixa.valor_liquido
        return Decimal("0.00") if saldo < 0 else saldo

    def _proximo_numero(self, prefixo, model):
        hoje = timezone.localdate().strftime("%Y%m%d")
        sequencial = model.objects.filter(numero_lancamento__startswith=f"{prefixo}-{hoje}").count() + 1
        return f"{prefixo}-{hoje}-{sequencial:04d}"

    def _somar_meses(self, data, meses):
        month = data.month - 1 + meses
        year = data.year + month // 12
        month = month % 12 + 1
        day = min(data.day, monthrange(year, month)[1])
        return data.replace(year=year, month=month, day=day)
