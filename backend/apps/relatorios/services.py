import hashlib
import json
from datetime import timedelta

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.relatorios.enums import FormatoExportacao, StatusExportacao, TipoDashboard, TipoRelatorio
from apps.relatorios.exports.csv_exporter import CSVExporter
from apps.relatorios.exports.excel_exporter import ExcelExporter
from apps.relatorios.exports.pdf_exporter import PDFExporter
from apps.relatorios.models import DashboardCache, ExportacaoArquivo, RelatorioGerado, RelatoriosRecord
from apps.relatorios.selectors import (
    comercial_indicadores,
    estoque_indicadores,
    executivo_indicadores,
    financeiro_indicadores,
    operacional_indicadores,
    relatorio_comercial,
    relatorio_compras,
    relatorio_estoque,
    relatorio_financeiro,
    relatorio_os,
)


def create_record(*, name, description="", created_by=None):
    return RelatoriosRecord.objects.create(name=name, description=description, created_by=created_by)


class DashboardService:
    dashboard_map = {
        TipoDashboard.EXECUTIVO: executivo_indicadores,
        TipoDashboard.FINANCEIRO: financeiro_indicadores,
        TipoDashboard.ESTOQUE: estoque_indicadores,
        TipoDashboard.COMERCIAL: comercial_indicadores,
        TipoDashboard.OPERACIONAL: operacional_indicadores,
    }

    def consolidar(self, *, tipo_dashboard, filtros=None, usuario=None):
        filtros = filtros or {}
        chave = self._cache_key(tipo_dashboard, filtros)
        cached = cache.get(chave)
        if cached:
            return cached

        cache_db = DashboardCache.objects.filter(chave=chave, expires_at__gt=timezone.now()).first()
        if cache_db:
            cache.set(chave, cache_db.payload, timeout=300)
            return cache_db.payload

        payload = self.dashboard_map[tipo_dashboard](filtros)
        payload = {"tipo": tipo_dashboard, "filtros": filtros, "indicadores": payload, "gerado_em": timezone.now().isoformat()}
        payload = json.loads(json.dumps(payload, default=str))
        DashboardCache.objects.update_or_create(
            chave=chave,
            defaults={
                "tipo_dashboard": tipo_dashboard,
                "filtros": filtros,
                "payload": payload,
                "expires_at": timezone.now() + timedelta(minutes=10),
                "gerado_por": usuario,
            },
        )
        cache.set(chave, payload, timeout=600)
        return payload

    def _cache_key(self, tipo_dashboard, filtros):
        raw = json.dumps({"tipo": tipo_dashboard, "filtros": filtros}, sort_keys=True, default=str)
        return f"dashboard:{tipo_dashboard}:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"


class RelatorioService:
    report_map = {
        TipoRelatorio.FINANCEIRO: ("Relatorio financeiro", relatorio_financeiro),
        TipoRelatorio.ESTOQUE: ("Relatorio de estoque", relatorio_estoque),
        TipoRelatorio.COMERCIAL: ("Relatorio comercial", relatorio_comercial),
        TipoRelatorio.OS: ("Relatorio de ordens de servico", relatorio_os),
        TipoRelatorio.COMPRAS: ("Relatorio de compras", relatorio_compras),
    }
    exporter_map = {
        FormatoExportacao.PDF: PDFExporter(),
        FormatoExportacao.EXCEL: ExcelExporter(),
        FormatoExportacao.CSV: CSVExporter(),
    }

    @transaction.atomic
    def gerar_relatorio(self, *, tipo_relatorio, filtros=None, usuario):
        if tipo_relatorio not in self.report_map:
            raise ValidationError("Tipo de relatorio invalido.")
        filtros = filtros or {}
        titulo, builder = self.report_map[tipo_relatorio]
        payload = builder(filtros)
        return RelatorioGerado.objects.create(
            tipo_relatorio=tipo_relatorio,
            titulo=titulo,
            filtros=filtros,
            payload=json.loads(json.dumps(payload, default=str)),
            gerado_por=usuario,
            created_by=usuario,
            updated_by=usuario,
        )

    @transaction.atomic
    def solicitar_exportacao(self, *, tipo_relatorio, formato, filtros=None, usuario):
        self._validar_limite_exportacoes(usuario)
        exportacao = ExportacaoArquivo.objects.create(
            tipo_relatorio=tipo_relatorio,
            formato=formato,
            filtros=filtros or {},
            solicitado_por=usuario,
            created_by=usuario,
            updated_by=usuario,
        )
        return self.processar_exportacao(exportacao_id=exportacao.id)

    @transaction.atomic
    def processar_exportacao(self, *, exportacao_id):
        exportacao = ExportacaoArquivo.objects.select_for_update().get(id=exportacao_id)
        exportacao.status = StatusExportacao.PROCESSANDO
        exportacao.save(update_fields=["status", "updated_at"])
        try:
            relatorio = self.gerar_relatorio(tipo_relatorio=exportacao.tipo_relatorio, filtros=exportacao.filtros, usuario=exportacao.solicitado_por)
            exporter = self.exporter_map[exportacao.formato]
            filename, content = exporter.export(relatorio)
            exportacao.relatorio = relatorio
            exportacao.arquivo.save(filename, content, save=False)
            exportacao.status = StatusExportacao.CONCLUIDA
            exportacao.erro = ""
        except Exception as exc:
            exportacao.status = StatusExportacao.FALHOU
            exportacao.erro = str(exc)
        exportacao.save(update_fields=["relatorio", "arquivo", "status", "erro", "updated_at"])
        return exportacao

    def _validar_limite_exportacoes(self, usuario):
        pendentes = ExportacaoArquivo.objects.filter(solicitado_por=usuario, status__in=[StatusExportacao.PENDENTE, StatusExportacao.PROCESSANDO]).count()
        if pendentes >= 3:
            raise ValidationError("Limite de exportacoes simultaneas atingido.")
