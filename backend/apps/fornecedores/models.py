from django.conf import settings
from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.clientes.enums import StatusRelacionamento, TipoPessoa
from apps.fornecedores.enums import CategoriaFornecedor


class Fornecedor(TimeStampedModel, SoftDeleteModel, AuditModel):
    tipo_pessoa = models.CharField(max_length=20, choices=TipoPessoa.choices, default=TipoPessoa.JURIDICA)
    razao_social = models.CharField(max_length=180, db_index=True)
    nome_fantasia = models.CharField(max_length=180, blank=True)
    documento = models.CharField(max_length=20, db_index=True)
    inscricao_estadual = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(max_length=30, blank=True)
    categoria = models.CharField(max_length=30, choices=CategoriaFornecedor.choices, default=CategoriaFornecedor.OUTROS, db_index=True)
    status = models.CharField(max_length=20, choices=StatusRelacionamento.choices, default=StatusRelacionamento.ATIVO, db_index=True)
    observacoes = models.TextField(blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="fornecedores_responsavel")

    class Meta:
        ordering = ["razao_social"]
        constraints = [
            models.UniqueConstraint(fields=["documento"], condition=models.Q(is_active=True), name="fornecedores_documento_ativo_uniq"),
        ]
        indexes = [
            models.Index(fields=["razao_social", "is_active"]),
            models.Index(fields=["documento", "is_active"]),
            models.Index(fields=["status", "is_active"]),
            models.Index(fields=["categoria", "is_active"]),
        ]

    def __str__(self):
        return self.nome_fantasia or self.razao_social
