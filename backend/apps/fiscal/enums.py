from django.db import models


class AmbienteFiscal(models.TextChoices):
    HOMOLOGACAO = "homologacao", "Homologacao"
    PRODUCAO = "producao", "Producao"


class RegimeTributario(models.TextChoices):
    SIMPLES = "simples_nacional", "Simples Nacional"
    LUCRO_PRESUMIDO = "lucro_presumido", "Lucro Presumido"
    LUCRO_REAL = "lucro_real", "Lucro Real"


class TipoOperacao(models.TextChoices):
    VENDA = "venda", "Venda"
    COMPRA = "compra", "Compra"
    DEVOLUCAO = "devolucao", "Devolucao"
    REMESSA = "remessa", "Remessa"
    RETORNO = "retorno", "Retorno"
    BONIFICACAO = "bonificacao", "Bonificacao"
    AJUSTE = "ajuste", "Ajuste"


class StatusNFe(models.TextChoices):
    RASCUNHO = "rascunho", "Rascunho"
    VALIDADA = "validada", "Validada"
    ASSINADA = "assinada", "Assinada"
    ENVIADA = "enviada", "Enviada"
    AUTORIZADA = "autorizada", "Autorizada"
    REJEITADA = "rejeitada", "Rejeitada"
    CANCELADA = "cancelada", "Cancelada"
    DENEGADA = "denegada", "Denegada"


class TipoEventoFiscal(models.TextChoices):
    VALIDACAO = "validacao", "Validacao"
    ASSINATURA = "assinatura", "Assinatura"
    ENVIO = "envio", "Envio"
    AUTORIZACAO = "autorizacao", "Autorizacao"
    REJEICAO = "rejeicao", "Rejeicao"
    CANCELAMENTO = "cancelamento", "Cancelamento"
    ERRO_COMUNICACAO = "erro_comunicacao", "Erro de comunicacao"
    RETORNO_SEFAZ = "retorno_sefaz", "Retorno SEFAZ"
