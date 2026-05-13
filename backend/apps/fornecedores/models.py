from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel


class Fornecedor(TimeStampedModel, SoftDeleteModel, AuditModel):
    razao_social = models.CharField(max_length=180, db_index=True)
    nome_fantasia = models.CharField(max_length=180, blank=True)
    documento = models.CharField(max_length=20, unique=True, db_index=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["razao_social"]
        indexes = [
            models.Index(fields=["razao_social", "is_active"]),
            models.Index(fields=["documento", "is_active"]),
        ]

    def __str__(self):
        return self.nome_fantasia or self.razao_social
