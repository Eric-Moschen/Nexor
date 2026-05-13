from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRADOR = "administrador", "Administrador"
        FISCAL = "fiscal", "Fiscal"
        FINANCEIRO = "financeiro", "Financeiro"
        ESTOQUE = "estoque", "Estoque"
        COMPRAS = "compras", "Compras"
        OPERACIONAL = "operacional", "Operacional"
        SUPERVISOR = "supervisor", "Supervisor"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.OPERACIONAL)

    class Meta:
        ordering = ["first_name", "last_name", "username"]
        indexes = [models.Index(fields=["email"]), models.Index(fields=["role"])]


class LoginAudit(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_audits")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)
