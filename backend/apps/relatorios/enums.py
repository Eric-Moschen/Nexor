from django.db import models


class TipoDashboard(models.TextChoices):
    EXECUTIVO = "executivo", "Executivo"
    FINANCEIRO = "financeiro", "Financeiro"
    ESTOQUE = "estoque", "Estoque"
    COMERCIAL = "comercial", "Comercial"
    OPERACIONAL = "operacional", "Operacional"


class TipoRelatorio(models.TextChoices):
    FINANCEIRO = "financeiro", "Financeiro"
    ESTOQUE = "estoque", "Estoque"
    COMERCIAL = "comercial", "Comercial"
    OS = "os", "Ordens de servico"
    COMPRAS = "compras", "Compras"


class FormatoExportacao(models.TextChoices):
    PDF = "pdf", "PDF"
    EXCEL = "excel", "Excel"
    CSV = "csv", "CSV"


class StatusExportacao(models.TextChoices):
    PENDENTE = "pendente", "Pendente"
    PROCESSANDO = "processando", "Processando"
    CONCLUIDA = "concluida", "Concluida"
    FALHOU = "falhou", "Falhou"
