from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.clientes.models import Cliente
from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.estoque.models import Produto
from apps.orcamentos.enums import StatusOrcamento, TipoEventoOrcamento
from apps.ordens_servico.models import OrdemServico


class Orcamento(TimeStampedModel, SoftDeleteModel, AuditModel):
    numero = models.CharField(max_length=30, unique=True, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="orcamentos")
    titulo = models.CharField(max_length=180, db_index=True)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True, db_index=True)
    data_validade = models.DateField(db_index=True)
    status = models.CharField(max_length=30, choices=StatusOrcamento.choices, default=StatusOrcamento.RASCUNHO, db_index=True)
    condicao_pagamento = models.CharField(max_length=180, blank=True)
    prazo_entrega = models.CharField(max_length=120, blank=True)
    observacoes_internas = models.TextField(blank=True)
    observacoes_cliente = models.TextField(blank=True)
    valor_produtos = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_servicos = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_desconto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    custo_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    margem_estimada = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal("0.00"))
    motivo_reprovacao = models.TextField(blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orcamentos_responsavel")
    ordem_servico = models.OneToOneField(OrdemServico, null=True, blank=True, on_delete=models.PROTECT, related_name="orcamento_origem")
    pdf_gerado = models.FileField(upload_to="orcamentos/", blank=True)

    class Meta:
        ordering = ["-data_criacao", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(valor_produtos__gte=0), name="orc_valor_produtos_gte_0"),
            models.CheckConstraint(check=models.Q(valor_servicos__gte=0), name="orc_valor_servicos_gte_0"),
            models.CheckConstraint(check=models.Q(valor_desconto__gte=0), name="orc_valor_desconto_gte_0"),
            models.CheckConstraint(check=models.Q(valor_total__gte=0), name="orc_valor_total_gte_0"),
            models.CheckConstraint(check=models.Q(custo_total__gte=0), name="orc_custo_total_gte_0"),
        ]
        indexes = [
            models.Index(fields=["status", "data_criacao"]),
            models.Index(fields=["cliente", "status"]),
            models.Index(fields=["data_validade"]),
        ]

    def __str__(self):
        return f"{self.numero} - {self.titulo}"


class ItemProdutoOrcamento(TimeStampedModel):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="itens_produto")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="itens_orcamento")
    descricao = models.CharField(max_length=220)
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    custo_unitario = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0"))])
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    desconto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    custo_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="orc_item_prod_quantidade_gt_0"),
            models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="orc_item_prod_valor_unit_gte_0"),
            models.CheckConstraint(check=models.Q(custo_unitario__gte=0), name="orc_item_prod_custo_unit_gte_0"),
            models.CheckConstraint(check=models.Q(desconto__gte=0), name="orc_item_prod_desconto_gte_0"),
        ]


class ItemServicoOrcamento(TimeStampedModel):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="itens_servico")
    descricao = models.CharField(max_length=220)
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    custo_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    desconto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="orc_item_serv_quantidade_gt_0"),
            models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="orc_item_serv_valor_unit_gte_0"),
            models.CheckConstraint(check=models.Q(custo_estimado__gte=0), name="orc_item_serv_custo_gte_0"),
            models.CheckConstraint(check=models.Q(desconto__gte=0), name="orc_item_serv_desconto_gte_0"),
        ]


class HistoricoOrcamento(TimeStampedModel):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE, related_name="historico")
    tipo_evento = models.CharField(max_length=30, choices=TipoEventoOrcamento.choices, db_index=True)
    descricao = models.TextField()
    status_anterior = models.CharField(max_length=30, blank=True)
    status_novo = models.CharField(max_length=30, blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="historicos_orcamento")
    dados_extras = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["orcamento", "tipo_evento"])]
