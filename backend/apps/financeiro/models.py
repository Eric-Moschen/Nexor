from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.clientes.models import Cliente
from apps.compras.models import PedidoCompra
from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.financeiro.enums import StatusContaPagar, StatusContaReceber, TipoBaixa, TipoFinanceiro
from apps.fornecedores.models import Fornecedor


class CentroCusto(TimeStampedModel, SoftDeleteModel, AuditModel):
    codigo = models.CharField(max_length=30, unique=True, db_index=True)
    nome = models.CharField(max_length=120, db_index=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["codigo"]
        indexes = [models.Index(fields=["codigo", "is_active"])]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class CategoriaFinanceira(TimeStampedModel, SoftDeleteModel, AuditModel):
    nome = models.CharField(max_length=120, db_index=True)
    tipo = models.CharField(max_length=20, choices=TipoFinanceiro.choices, db_index=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["tipo", "nome"]
        constraints = [
            models.UniqueConstraint(fields=["nome", "tipo"], name="financeiro_categoria_nome_tipo_uniq"),
        ]
        indexes = [models.Index(fields=["tipo", "is_active"])]

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Parcelamento(TimeStampedModel, AuditModel):
    descricao = models.CharField(max_length=180)
    quantidade_parcelas = models.PositiveIntegerField()
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    data_primeiro_vencimento = models.DateField()
    intervalo_meses = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.descricao


class ContaPagar(TimeStampedModel, SoftDeleteModel, AuditModel):
    numero_lancamento = models.CharField(max_length=30, unique=True, db_index=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name="contas_pagar")
    descricao = models.CharField(max_length=220)
    categoria = models.ForeignKey(CategoriaFinanceira, on_delete=models.PROTECT, related_name="contas_pagar")
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.PROTECT, related_name="contas_pagar")
    valor_original = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    valor_atual = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    data_emissao = models.DateField()
    data_vencimento = models.DateField(db_index=True)
    status = models.CharField(max_length=30, choices=StatusContaPagar.choices, default=StatusContaPagar.PENDENTE, db_index=True)
    tipo_pagamento = models.CharField(max_length=80, blank=True)
    observacao = models.TextField(blank=True)
    pedido_compra_origem = models.ForeignKey(PedidoCompra, null=True, blank=True, on_delete=models.PROTECT, related_name="contas_pagar")
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contas_pagar_responsavel")
    parcelamento = models.ForeignKey(Parcelamento, null=True, blank=True, on_delete=models.PROTECT, related_name="contas_pagar")

    class Meta:
        ordering = ["data_vencimento", "numero_lancamento"]
        constraints = [
            models.CheckConstraint(check=models.Q(valor_original__gt=0), name="financeiro_cp_valor_original_gt_0"),
            models.CheckConstraint(check=models.Q(valor_atual__gte=0), name="financeiro_cp_valor_atual_gte_0"),
        ]
        indexes = [
            models.Index(fields=["status", "data_vencimento"]),
            models.Index(fields=["fornecedor", "status"]),
            models.Index(fields=["centro_custo", "status"]),
        ]

    def __str__(self):
        return self.numero_lancamento


class ContaReceber(TimeStampedModel, SoftDeleteModel, AuditModel):
    numero_lancamento = models.CharField(max_length=30, unique=True, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="contas_receber")
    descricao = models.CharField(max_length=220)
    categoria = models.ForeignKey(CategoriaFinanceira, on_delete=models.PROTECT, related_name="contas_receber")
    centro_custo = models.ForeignKey(CentroCusto, on_delete=models.PROTECT, related_name="contas_receber")
    valor_original = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    valor_atual = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    data_emissao = models.DateField()
    data_vencimento = models.DateField(db_index=True)
    status = models.CharField(max_length=30, choices=StatusContaReceber.choices, default=StatusContaReceber.PENDENTE, db_index=True)
    forma_recebimento = models.CharField(max_length=80, blank=True)
    observacao = models.TextField(blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="contas_receber_responsavel")
    parcelamento = models.ForeignKey(Parcelamento, null=True, blank=True, on_delete=models.PROTECT, related_name="contas_receber")

    class Meta:
        ordering = ["data_vencimento", "numero_lancamento"]
        constraints = [
            models.CheckConstraint(check=models.Q(valor_original__gt=0), name="financeiro_cr_valor_original_gt_0"),
            models.CheckConstraint(check=models.Q(valor_atual__gte=0), name="financeiro_cr_valor_atual_gte_0"),
        ]
        indexes = [
            models.Index(fields=["status", "data_vencimento"]),
            models.Index(fields=["cliente", "status"]),
            models.Index(fields=["centro_custo", "status"]),
        ]

    def __str__(self):
        return self.numero_lancamento


class BaixaFinanceira(TimeStampedModel):
    conta_pagar = models.ForeignKey(ContaPagar, null=True, blank=True, on_delete=models.PROTECT, related_name="baixas")
    conta_receber = models.ForeignKey(ContaReceber, null=True, blank=True, on_delete=models.PROTECT, related_name="baixas")
    tipo = models.CharField(max_length=20, choices=TipoBaixa.choices, db_index=True)
    valor_pago = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    data_pagamento = models.DateField(db_index=True)
    multa = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    juros = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    desconto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    observacao = models.TextField(blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="baixas_financeiras")

    class Meta:
        ordering = ["-data_pagamento", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(valor_pago__gt=0), name="financeiro_baixa_valor_gt_0"),
            models.CheckConstraint(check=models.Q(multa__gte=0), name="financeiro_baixa_multa_gte_0"),
            models.CheckConstraint(check=models.Q(juros__gte=0), name="financeiro_baixa_juros_gte_0"),
            models.CheckConstraint(check=models.Q(desconto__gte=0), name="financeiro_baixa_desconto_gte_0"),
        ]
        indexes = [
            models.Index(fields=["tipo", "data_pagamento"]),
            models.Index(fields=["conta_pagar"]),
            models.Index(fields=["conta_receber"]),
        ]

    @property
    def valor_liquido(self):
        return self.valor_pago + self.multa + self.juros - self.desconto
