from django.db import models


class StatusOrcamento(models.TextChoices):
    RASCUNHO = "rascunho", "Rascunho"
    EM_ANALISE = "em_analise", "Em analise"
    ENVIADO = "enviado", "Enviado"
    APROVADO = "aprovado", "Aprovado"
    REPROVADO = "reprovado", "Reprovado"
    EXPIRADO = "expirado", "Expirado"
    CONVERTIDO_OS = "convertido_os", "Convertido em OS"
    CANCELADO = "cancelado", "Cancelado"


class TipoEventoOrcamento(models.TextChoices):
    CRIACAO = "criacao", "Criacao"
    ALTERACAO = "alteracao", "Alteracao"
    ENVIO = "envio", "Envio"
    APROVACAO = "aprovacao", "Aprovacao"
    REPROVACAO = "reprovacao", "Reprovacao"
    CANCELAMENTO = "cancelamento", "Cancelamento"
    EXPIRACAO = "expiracao", "Expiracao"
    CONVERSAO_OS = "conversao_os", "Conversao em OS"
    PDF = "pdf", "Geracao de PDF"
