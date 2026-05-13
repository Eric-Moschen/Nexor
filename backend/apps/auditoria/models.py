from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel


class AuditoriaRecord(TimeStampedModel, SoftDeleteModel, AuditModel):
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name", "is_active"])]

    def __str__(self):
        return self.name
