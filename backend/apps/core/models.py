"""Shared abstract models for domain apps."""
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class TenantReadyModel(TimeStampedModel, SoftDeleteModel):
    """Base model prepared for future company/tenant linkage."""

    class Meta:
        abstract = True
