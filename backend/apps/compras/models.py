from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.estoque.models import Produto, UnidadeMedida
from apps.fornecedores.models import Fornecedor


class SolicitacaoCompra(TimeStampedModel, SoftDeleteModel, AuditModel):
    class Status(models.TextChoices):
        RASCUNHO = "rascunho", "Rascunho"
        PENDENTE = "pendente_aprovacao", "Pendente de aprovacao"
        APROVADA = "aprovada", "Aprovada"
        REPROVADA = "reprovada", "Reprovada"
        CONVERTIDA = "convertida_pedido", "Convertida em pedido"
        CANCELADA = "cancelada", "Cancelada"

    class Prioridade(models.TextChoices):
        BAIXA = "baixa", "Baixa"
        MEDIA = "media", "Media"
        ALTA = "alta", "Alta"
        URGENTE = "urgente", "Urgente"

    numero = models.CharField(max_length=30, unique=True, db_index=True)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="solicitacoes_compra")
    centro_custo = models.CharField(max_length=120)
    justificativa = models.TextField()
    prioridade = models.CharField(max_length=20, choices=Prioridade.choices, default=Prioridade.MEDIA)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.RASCUNHO, db_index=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True, db_index=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    aprovador = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="aprovacoes_compra")
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_solicitacao", "-id"]
        indexes = [
            models.Index(fields=["numero", "status"]),
            models.Index(fields=["solicitante", "status"]),
            models.Index(fields=["data_solicitacao"]),
        ]

    def __str__(self):
        return self.numero


class ItemSolicitacaoCompra(TimeStampedModel):
    class Status(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        APROVADO = "aprovado", "Aprovado"
        REPROVADO = "reprovado", "Reprovado"
        CONVERTIDO = "convertido", "Convertido"

    solicitacao = models.ForeignKey(SolicitacaoCompra, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.PROTECT, related_name="itens_solicitacao_compra")
    descricao_livre = models.CharField(max_length=220, blank=True)
    quantidade_solicitada = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.PROTECT, related_name="itens_solicitacao_compra")
    observacao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTO, db_index=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade_solicitada__gt=0), name="compras_item_solic_qtd_gt_0"),
        ]
        indexes = [
            models.Index(fields=["solicitacao", "status"]),
            models.Index(fields=["produto"]),
        ]

    def __str__(self):
        return self.descricao_livre or str(self.produto)


class PedidoCompra(TimeStampedModel, SoftDeleteModel, AuditModel):
    class Status(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        ENVIADO = "enviado_fornecedor", "Enviado ao fornecedor"
        PARCIAL = "parcialmente_recebido", "Parcialmente recebido"
        RECEBIDO = "recebido", "Recebido"
        CANCELADO = "cancelado", "Cancelado"

    numero = models.CharField(max_length=30, unique=True, db_index=True)
    solicitacao_origem = models.OneToOneField(SolicitacaoCompra, null=True, blank=True, on_delete=models.PROTECT, related_name="pedido")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name="pedidos_compra")
    data_pedido = models.DateTimeField(auto_now_add=True, db_index=True)
    previsao_entrega = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ABERTO, db_index=True)
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    observacoes = models.TextField(blank=True)

    class Meta:
        ordering = ["-data_pedido", "-id"]
        indexes = [
            models.Index(fields=["numero", "status"]),
            models.Index(fields=["fornecedor", "status"]),
            models.Index(fields=["data_pedido"]),
        ]

    def __str__(self):
        return self.numero


class ItemPedidoCompra(TimeStampedModel):
    pedido = models.ForeignKey(PedidoCompra, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.PROTECT, related_name="itens_pedido_compra")
    descricao = models.CharField(max_length=220)
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    unidade_medida = models.ForeignKey(UnidadeMedida, on_delete=models.PROTECT, related_name="itens_pedido_compra")
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    quantidade_recebida = models.DecimalField(max_digits=14, decimal_places=4, default=Decimal("0.0000"), validators=[MinValueValidator(Decimal("0"))])

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="compras_item_pedido_qtd_gt_0"),
            models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="compras_item_pedido_vu_gte_0"),
            models.CheckConstraint(check=models.Q(quantidade_recebida__gte=0), name="compras_item_pedido_qtd_rec_gte_0"),
        ]
        indexes = [
            models.Index(fields=["pedido"]),
            models.Index(fields=["produto"]),
        ]

    def __str__(self):
        return self.descricao


class HistoricoAprovacaoCompra(TimeStampedModel):
    class Acao(models.TextChoices):
        ENVIAR = "enviar_aprovacao", "Enviar para aprovacao"
        APROVAR = "aprovar", "Aprovar"
        REPROVAR = "reprovar", "Reprovar"
        CANCELAR = "cancelar", "Cancelar"
        CONVERTER = "converter_pedido", "Converter em pedido"

    solicitacao = models.ForeignKey(SolicitacaoCompra, on_delete=models.CASCADE, related_name="historico_aprovacao")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    acao = models.CharField(max_length=30, choices=Acao.choices)
    status_anterior = models.CharField(max_length=30, blank=True)
    status_posterior = models.CharField(max_length=30)
    motivo = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["solicitacao", "acao"]),
            models.Index(fields=["created_at"]),
        ]
