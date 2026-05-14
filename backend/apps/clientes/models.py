from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.clientes.enums import StatusInteracaoCRM, StatusRelacionamento, TipoEndereco, TipoHistoricoRelacionamento, TipoInteracaoCRM, TipoPessoa


class Cliente(TimeStampedModel, SoftDeleteModel, AuditModel):
    tipo_pessoa = models.CharField(max_length=20, choices=TipoPessoa.choices, default=TipoPessoa.JURIDICA)
    razao_social = models.CharField(max_length=180, db_index=True)
    nome_fantasia = models.CharField(max_length=180, blank=True)
    documento = models.CharField(max_length=20, db_index=True)
    inscricao_estadual = models.CharField(max_length=30, blank=True)
    inscricao_municipal = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=20, choices=StatusRelacionamento.choices, default=StatusRelacionamento.ATIVO, db_index=True)
    limite_credito = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    observacoes = models.TextField(blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="clientes_responsavel")

    class Meta:
        ordering = ["razao_social"]
        constraints = [
            models.UniqueConstraint(fields=["documento"], condition=models.Q(is_active=True), name="clientes_documento_ativo_uniq"),
            models.CheckConstraint(check=models.Q(limite_credito__gte=0), name="clientes_limite_credito_gte_0"),
        ]
        indexes = [
            models.Index(fields=["razao_social", "is_active"]),
            models.Index(fields=["documento", "is_active"]),
            models.Index(fields=["status", "is_active"]),
        ]

    def __str__(self):
        return self.nome_fantasia or self.razao_social


class EnderecoRelacionamento(TimeStampedModel, SoftDeleteModel, AuditModel):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE, related_name="enderecos")
    fornecedor = models.ForeignKey("fornecedores.Fornecedor", null=True, blank=True, on_delete=models.CASCADE, related_name="enderecos")
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=180)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=120, blank=True)
    bairro = models.CharField(max_length=120)
    cidade = models.CharField(max_length=120)
    uf = models.CharField(max_length=2)
    codigo_ibge = models.CharField(max_length=7, blank=True)
    tipo = models.CharField(max_length=20, choices=TipoEndereco.choices, default=TipoEndereco.COMERCIAL)

    class Meta:
        ordering = ["tipo", "cidade"]
        constraints = [
            models.CheckConstraint(
                check=(models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False)),
                name="rel_endereco_cliente_ou_fornecedor",
            )
        ]
        indexes = [models.Index(fields=["cliente", "tipo"]), models.Index(fields=["fornecedor", "tipo"]), models.Index(fields=["cep"])]


class ContatoRelacionamento(TimeStampedModel, SoftDeleteModel, AuditModel):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE, related_name="contatos")
    fornecedor = models.ForeignKey("fornecedores.Fornecedor", null=True, blank=True, on_delete=models.CASCADE, related_name="contatos")
    nome = models.CharField(max_length=140)
    cargo = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    observacao = models.TextField(blank=True)
    principal = models.BooleanField(default=False)

    class Meta:
        ordering = ["-principal", "nome"]
        constraints = [
            models.CheckConstraint(
                check=(models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False)),
                name="rel_contato_cliente_ou_fornecedor",
            )
        ]
        indexes = [models.Index(fields=["cliente", "principal"]), models.Index(fields=["fornecedor", "principal"]), models.Index(fields=["email"])]


class InteracaoCRM(TimeStampedModel, SoftDeleteModel, AuditModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="interacoes")
    tipo_interacao = models.CharField(max_length=20, choices=TipoInteracaoCRM.choices, db_index=True)
    descricao = models.TextField()
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="interacoes_crm")
    data = models.DateTimeField(db_index=True)
    proximo_contato = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusInteracaoCRM.choices, default=StatusInteracaoCRM.ABERTO, db_index=True)

    class Meta:
        ordering = ["-data", "-id"]
        indexes = [models.Index(fields=["cliente", "status"]), models.Index(fields=["responsavel", "data"])]


class HistoricoRelacionamento(TimeStampedModel):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE, related_name="historico_relacionamento")
    fornecedor = models.ForeignKey("fornecedores.Fornecedor", null=True, blank=True, on_delete=models.CASCADE, related_name="historico_relacionamento")
    tipo_evento = models.CharField(max_length=30, choices=TipoHistoricoRelacionamento.choices, db_index=True)
    descricao = models.TextField()
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="historicos_relacionamento")
    dados_extras = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                check=(models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False)),
                name="rel_historico_cliente_ou_fornecedor",
            )
        ]
        indexes = [models.Index(fields=["cliente", "tipo_evento"]), models.Index(fields=["fornecedor", "tipo_evento"])]


class DocumentoRelacionamento(TimeStampedModel, SoftDeleteModel, AuditModel):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE, related_name="documentos")
    fornecedor = models.ForeignKey("fornecedores.Fornecedor", null=True, blank=True, on_delete=models.CASCADE, related_name="documentos")
    tipo_documento = models.CharField(max_length=80)
    titulo = models.CharField(max_length=160)
    arquivo = models.FileField(upload_to="relacionamentos/")
    observacao = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                check=(models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False)),
                name="rel_documento_cliente_ou_fornecedor",
            )
        ]
