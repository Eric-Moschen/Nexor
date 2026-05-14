from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRADOR = "administrador", "Administrador"
        DIRETORIA = "diretoria", "Diretoria"
        COMERCIAL = "comercial", "Comercial"
        FISCAL = "fiscal", "Fiscal"
        FINANCEIRO = "financeiro", "Financeiro"
        ESTOQUE = "estoque", "Estoque"
        COMPRAS = "compras", "Compras"
        OPERACIONAL = "operacional", "Operacional"
        SUPERVISOR = "supervisor", "Supervisor"

    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=30, blank=True)
    cargo = models.CharField(max_length=120, blank=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.OPERACIONAL)

    class Meta:
        ordering = ["first_name", "last_name", "username"]
        indexes = [models.Index(fields=["email"]), models.Index(fields=["role"])]

    @property
    def nome_completo(self):
        return self.get_full_name() or self.username

    def has_rbac_permission(self, permission_code):
        if not permission_code or self.is_superuser or self.role == self.Role.ADMINISTRADOR:
            return True
        return Permission.objects.filter(roles__role__role_users__user=self, code=permission_code, is_active=True).exists()


class Role(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["code", "is_active"])]

    def __str__(self):
        return self.name


class Permission(TimeStampedModel):
    code = models.CharField(max_length=120, unique=True, db_index=True)
    module = models.CharField(max_length=60, db_index=True)
    action = models.CharField(max_length=60, db_index=True)
    description = models.CharField(max_length=180, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["module", "code"]
        indexes = [models.Index(fields=["module", "action", "is_active"])]

    def __str__(self):
        return self.code


class RolePermission(TimeStampedModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="roles")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["role", "permission"], name="accounts_role_permission_uniq")]
        indexes = [models.Index(fields=["role", "permission"])]


class UserRole(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="role_memberships")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="role_users")
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "role"], name="accounts_user_role_uniq")]
        indexes = [models.Index(fields=["user", "is_primary"])]


class LoginAudit(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_audits")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=True)


class AuthAuditLog(TimeStampedModel):
    class Event(models.TextChoices):
        LOGIN_SUCCESS = "login_success", "Login realizado"
        LOGIN_FAILED = "login_failed", "Login falhou"
        LOGOUT = "logout", "Logout"
        PASSWORD_CHANGE = "password_change", "Troca de senha"

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="auth_audit_logs")
    event = models.CharField(max_length=30, choices=Event.choices, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    username_attempted = models.CharField(max_length=180, blank=True)
    success = models.BooleanField(default=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["user", "event"]), models.Index(fields=["event", "created_at"])]
