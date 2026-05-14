from django.conf import settings
from django.db import models

from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.relatorios.enums import FormatoExportacao, StatusExportacao, TipoDashboard, TipoRelatorio


class RelatoriosRecord(TimeStampedModel, SoftDeleteModel, AuditModel):
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["name", "is_active"])]

    def __str__(self):
        return self.name


class DashboardCache(TimeStampedModel):
    chave = models.CharField(max_length=180, unique=True, db_index=True)
    tipo_dashboard = models.CharField(max_length=30, choices=TipoDashboard.choices, db_index=True)
    filtros = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    expires_at = models.DateTimeField(db_index=True)
    gerado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="dashboards_cache")

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["tipo_dashboard", "expires_at"]),
        ]

    def __str__(self):
        return self.chave


class RelatorioGerado(TimeStampedModel, SoftDeleteModel, AuditModel):
    tipo_relatorio = models.CharField(max_length=30, choices=TipoRelatorio.choices, db_index=True)
    titulo = models.CharField(max_length=180)
    filtros = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    gerado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="relatorios_gerados")

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["tipo_relatorio", "created_at"]),
            models.Index(fields=["gerado_por", "created_at"]),
        ]

    def __str__(self):
        return self.titulo


class ExportacaoArquivo(TimeStampedModel, SoftDeleteModel, AuditModel):
    relatorio = models.ForeignKey(RelatorioGerado, null=True, blank=True, on_delete=models.SET_NULL, related_name="exportacoes")
    tipo_relatorio = models.CharField(max_length=30, choices=TipoRelatorio.choices, db_index=True)
    formato = models.CharField(max_length=10, choices=FormatoExportacao.choices, db_index=True)
    status = models.CharField(max_length=20, choices=StatusExportacao.choices, default=StatusExportacao.PENDENTE, db_index=True)
    filtros = models.JSONField(default=dict, blank=True)
    arquivo = models.FileField(upload_to="relatorios/", blank=True)
    erro = models.TextField(blank=True)
    task_id = models.CharField(max_length=120, blank=True, db_index=True)
    solicitado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="exportacoes_relatorios")

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["solicitado_por", "status"]),
            models.Index(fields=["tipo_relatorio", "formato"]),
        ]

    def __str__(self):
        return f"{self.tipo_relatorio}.{self.formato} - {self.status}"
