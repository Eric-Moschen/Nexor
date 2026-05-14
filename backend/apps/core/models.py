from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class AuditModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="%(class)s_updated")

    class Meta:
        abstract = True


class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = "create", "Criacao"
        UPDATE = "update", "Atualizacao"
        DELETE = "delete", "Exclusao logica"
        APPROVE = "approve", "Aprovacao"
        CANCEL = "cancel", "Cancelamento"
        LOGIN = "login", "Login"
        FISCAL = "fiscal", "Emissao fiscal"
        FINANCIAL = "financial", "Movimentacao financeira"
        STOCK = "stock", "Movimentacao estoque"
        SYSTEM = "system", "Sistema"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="global_audit_logs")
    action = models.CharField(max_length=30, choices=Action.choices, db_index=True)
    module = models.CharField(max_length=80, db_index=True)
    record_model = models.CharField(max_length=120, db_index=True)
    record_id = models.CharField(max_length=80, blank=True, db_index=True)
    record_repr = models.CharField(max_length=220, blank=True)
    before = models.JSONField(default=dict, blank=True)
    after = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["module", "action", "created_at"]),
            models.Index(fields=["record_model", "record_id"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        return f"{self.module}.{self.action} #{self.record_id}"


class EventLog(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        PROCESSED = "processed", "Processado"
        PARTIAL = "partial", "Parcial"
        FAILED = "failed", "Falhou"

    event_name = models.CharField(max_length=80, db_index=True)
    module = models.CharField(max_length=80, db_index=True)
    aggregate_type = models.CharField(max_length=120, db_index=True)
    aggregate_id = models.CharField(max_length=80, blank=True, db_index=True)
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    handlers_processed = models.JSONField(default=list, blank=True)
    error_message = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="event_logs")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["event_name", "status"]),
            models.Index(fields=["module", "created_at"]),
            models.Index(fields=["aggregate_type", "aggregate_id"]),
        ]

    def mark_processed(self, handlers):
        self.status = self.Status.PROCESSED
        self.handlers_processed = handlers
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "handlers_processed", "processed_at"])

    def mark_partial(self, handlers, error_message):
        self.status = self.Status.PARTIAL
        self.handlers_processed = handlers
        self.error_message = error_message
        self.processed_at = timezone.now()
        self.save(update_fields=["status", "handlers_processed", "error_message", "processed_at"])

    def __str__(self):
        return f"{self.event_name} - {self.status}"


class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = "info", "Informacao"
        SUCCESS = "success", "Sucesso"
        WARNING = "warning", "Aviso"
        CRITICAL = "critical", "Critico"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=160)
    message = models.TextField()
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.INFO, db_index=True)
    category = models.CharField(max_length=80, db_index=True)
    event = models.ForeignKey(EventLog, null=True, blank=True, on_delete=models.SET_NULL, related_name="notifications")
    metadata = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["recipient", "is_read", "created_at"]),
            models.Index(fields=["category", "level"]),
        ]

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])

    def __str__(self):
        return self.title
