from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel


class CategoriaProduto(TimeStampedModel, SoftDeleteModel, AuditModel):
    nome = models.CharField(max_length=120, unique=True, db_index=True)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["nome"]
        indexes = [
            models.Index(fields=["nome", "is_active"]),
        ]

    def __str__(self):
        return self.nome


class UnidadeMedida(TimeStampedModel, SoftDeleteModel, AuditModel):
    sigla = models.CharField(max_length=10, unique=True, db_index=True)
    nome = models.CharField(max_length=80)
    descricao = models.TextField(blank=True)

    class Meta:
        ordering = ["sigla"]
        indexes = [
            models.Index(fields=["sigla", "is_active"]),
        ]

    def __str__(self):
        return self.sigla


class Produto(TimeStampedModel, SoftDeleteModel, AuditModel):
    codigo_interno = models.CharField(max_length=40, unique=True, db_index=True)
    sku = models.CharField(max_length=60, unique=True, db_index=True)
    codigo_barras = models.CharField(max_length=80, blank=True, db_index=True)
    nome = models.CharField(max_length=180, db_index=True)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(
        CategoriaProduto,
        on_delete=models.PROTECT,
        related_name="produtos",
    )
    unidade_medida = models.ForeignKey(
        UnidadeMedida,
        on_delete=models.PROTECT,
        related_name="produtos",
    )
    marca = models.CharField(max_length=120, blank=True)
    custo_medio = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=Decimal("0.0000"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    preco_venda = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    estoque_minimo = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=Decimal("0.0000"),
        validators=[MinValueValidator(Decimal("0"))],
    )
    estoque_atual = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=Decimal("0.0000"),
        validators=[MinValueValidator(Decimal("0"))],
    )

    class Meta:
        ordering = ["nome"]
        constraints = [
            models.CheckConstraint(check=models.Q(estoque_minimo__gte=0), name="estoque_produto_minimo_gte_0"),
            models.CheckConstraint(check=models.Q(estoque_atual__gte=0), name="estoque_produto_atual_gte_0"),
            models.CheckConstraint(check=models.Q(custo_medio__gte=0), name="estoque_produto_custo_gte_0"),
            models.CheckConstraint(check=models.Q(preco_venda__gte=0), name="estoque_produto_preco_gte_0"),
        ]
        indexes = [
            models.Index(fields=["nome", "is_active"]),
            models.Index(fields=["codigo_interno", "is_active"]),
            models.Index(fields=["sku", "is_active"]),
            models.Index(fields=["categoria", "is_active"]),
        ]

    def __str__(self):
        return f"{self.codigo_interno} - {self.nome}"


class MovimentacaoEstoque(TimeStampedModel):
    class Tipo(models.TextChoices):
        ENTRADA = "entrada", "Entrada"
        SAIDA = "saida", "Saida"
        AJUSTE = "ajuste", "Ajuste"
        TRANSFERENCIA = "transferencia", "Transferencia"

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="movimentacoes")
    tipo = models.CharField(max_length=20, choices=Tipo.choices, db_index=True)
    quantidade = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )
    saldo_anterior = models.DecimalField(max_digits=14, decimal_places=4)
    saldo_posterior = models.DecimalField(max_digits=14, decimal_places=4)
    usuario_responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movimentacoes_estoque",
    )
    observacao = models.TextField(blank=True)
    data_movimentacao = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-data_movimentacao", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="estoque_mov_quantidade_gt_0"),
            models.CheckConstraint(check=models.Q(saldo_posterior__gte=0), name="estoque_mov_saldo_posterior_gte_0"),
        ]
        indexes = [
            models.Index(fields=["produto", "tipo"]),
            models.Index(fields=["data_movimentacao"]),
        ]

    def __str__(self):
        return f"{self.produto_id} {self.tipo} {self.quantidade}"
