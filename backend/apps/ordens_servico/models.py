from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.clientes.models import Cliente
from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.estoque.models import Produto
from apps.financeiro.models import CategoriaFinanceira, CentroCusto, ContaReceber
from apps.ordens_servico.enums import PrioridadeOS, StatusOS, TipoEventoOS, TipoHoraOS


class OrdemServico(TimeStampedModel, SoftDeleteModel, AuditModel):
    numero = models.CharField(max_length=30, unique=True, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ordens_servico")
    titulo = models.CharField(max_length=180, db_index=True)
    descricao_servico = models.TextField()
    tipo_servico = models.CharField(max_length=80, db_index=True)
    prioridade = models.CharField(max_length=20, choices=PrioridadeOS.choices, default=PrioridadeOS.MEDIA, db_index=True)
    status = models.CharField(max_length=30, choices=StatusOS.choices, default=StatusOS.RASCUNHO, db_index=True)
    data_abertura = models.DateTimeField(auto_now_add=True, db_index=True)
    data_prevista = models.DateField(null=True, blank=True, db_index=True)
    data_inicio = models.DateTimeField(null=True, blank=True)
    data_finalizacao = models.DateTimeField(null=True, blank=True)
    responsavel_tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="ordens_responsavel")
    observacoes = models.TextField(blank=True)
    valor_estimado = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_final = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    custo_materiais = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    custo_mao_obra = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    custo_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    usuario_criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ordens_criadas")
    categoria_financeira = models.ForeignKey(CategoriaFinanceira, null=True, blank=True, on_delete=models.PROTECT, related_name="ordens_servico")
    centro_custo = models.ForeignKey(CentroCusto, null=True, blank=True, on_delete=models.PROTECT, related_name="ordens_servico")
    conta_receber = models.ForeignKey(ContaReceber, null=True, blank=True, on_delete=models.PROTECT, related_name="ordens_servico")
    nota_fiscal = models.ForeignKey("fiscal.NotaFiscal", null=True, blank=True, on_delete=models.PROTECT, related_name="ordens_servico")

    class Meta:
        ordering = ["-data_abertura", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(valor_estimado__gte=0), name="os_valor_estimado_gte_0"),
            models.CheckConstraint(check=models.Q(valor_final__gte=0), name="os_valor_final_gte_0"),
            models.CheckConstraint(check=models.Q(custo_materiais__gte=0), name="os_custo_materiais_gte_0"),
            models.CheckConstraint(check=models.Q(custo_mao_obra__gte=0), name="os_custo_mao_obra_gte_0"),
            models.CheckConstraint(check=models.Q(custo_total__gte=0), name="os_custo_total_gte_0"),
        ]
        indexes = [
            models.Index(fields=["status", "data_abertura"]),
            models.Index(fields=["cliente", "status"]),
            models.Index(fields=["prioridade", "status"]),
            models.Index(fields=["data_prevista"]),
        ]

    def __str__(self):
        return f"{self.numero} - {self.titulo}"


class ItemServico(TimeStampedModel):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name="itens")
    descricao = models.CharField(max_length=220)
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="os_item_quantidade_gt_0"),
            models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="os_item_valor_unitario_gte_0"),
        ]

    def __str__(self):
        return self.descricao


class MaterialUtilizadoOS(TimeStampedModel):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.PROTECT, related_name="materiais")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="materiais_os")
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    custo_unitario = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0"))])
    custo_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    data_utilizacao = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="materiais_os")

    class Meta:
        ordering = ["-data_utilizacao", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="os_material_quantidade_gt_0"),
            models.CheckConstraint(check=models.Q(custo_unitario__gte=0), name="os_material_custo_unitario_gte_0"),
        ]
        indexes = [models.Index(fields=["ordem_servico", "produto"])]


class ApontamentoHorasOS(TimeStampedModel):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name="apontamentos")
    colaborador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="apontamentos_os")
    data = models.DateField(db_index=True)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    total_horas = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    tipo_hora = models.CharField(max_length=20, choices=TipoHoraOS.choices, default=TipoHoraOS.NORMAL)
    custo_hora = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    custo_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["-data", "-hora_inicio", "-id"]
        constraints = [
            models.CheckConstraint(check=models.Q(hora_fim__gt=models.F("hora_inicio")), name="os_apontamento_hora_fim_gt_inicio"),
            models.CheckConstraint(check=models.Q(total_horas__gte=0), name="os_apontamento_total_horas_gte_0"),
        ]
        indexes = [
            models.Index(fields=["colaborador", "data"]),
            models.Index(fields=["ordem_servico", "data"]),
        ]


class HistoricoOS(TimeStampedModel):
    ordem_servico = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, related_name="historico")
    tipo_evento = models.CharField(max_length=30, choices=TipoEventoOS.choices, db_index=True)
    descricao = models.TextField()
    status_anterior = models.CharField(max_length=30, blank=True)
    status_novo = models.CharField(max_length=30, blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="historicos_os")
    dados_extras = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["ordem_servico", "tipo_evento"])]
