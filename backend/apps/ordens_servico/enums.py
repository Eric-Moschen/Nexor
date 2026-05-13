from django.db import models


class StatusOS(models.TextChoices):
    RASCUNHO = "rascunho", "Rascunho"
    ABERTA = "aberta", "Aberta"
    EM_APROVACAO = "em_aprovacao", "Em aprovacao"
    APROVADA = "aprovada", "Aprovada"
    EM_EXECUCAO = "em_execucao", "Em execucao"
    PAUSADA = "pausada", "Pausada"
    FINALIZADA = "finalizada", "Finalizada"
    CANCELADA = "cancelada", "Cancelada"
    FATURADA = "faturada", "Faturada"


class PrioridadeOS(models.TextChoices):
    BAIXA = "baixa", "Baixa"
    MEDIA = "media", "Media"
    ALTA = "alta", "Alta"
    URGENTE = "urgente", "Urgente"


class TipoHoraOS(models.TextChoices):
    NORMAL = "normal", "Normal"
    EXTRA_50 = "extra_50", "Extra 50%"
    EXTRA_100 = "extra_100", "Extra 100%"


class TipoEventoOS(models.TextChoices):
    CRIACAO = "criacao", "Criacao"
    ENVIO_APROVACAO = "envio_aprovacao", "Envio para aprovacao"
    APROVACAO = "aprovacao", "Aprovacao"
    INICIO = "inicio", "Inicio"
    PAUSA = "pausa", "Pausa"
    RETOMADA = "retomada", "Retomada"
    MATERIAL = "material", "Uso de material"
    APONTAMENTO = "apontamento", "Apontamento de horas"
    ALTERACAO_STATUS = "alteracao_status", "Alteracao de status"
    FINALIZACAO = "finalizacao", "Finalizacao"
    CANCELAMENTO = "cancelamento", "Cancelamento"
    FATURAMENTO = "faturamento", "Faturamento"
    ESTORNO_MATERIAL = "estorno_material", "Estorno de material"
