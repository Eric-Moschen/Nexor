from django.db import models


class TipoPessoa(models.TextChoices):
    FISICA = "fisica", "Pessoa Fisica"
    JURIDICA = "juridica", "Pessoa Juridica"


class StatusRelacionamento(models.TextChoices):
    ATIVO = "ativo", "Ativo"
    INATIVO = "inativo", "Inativo"
    BLOQUEADO = "bloqueado", "Bloqueado"


class TipoEndereco(models.TextChoices):
    COMERCIAL = "comercial", "Comercial"
    COBRANCA = "cobranca", "Cobranca"
    ENTREGA = "entrega", "Entrega"
    FISCAL = "fiscal", "Fiscal"


class TipoInteracaoCRM(models.TextChoices):
    LIGACAO = "ligacao", "Ligacao"
    WHATSAPP = "whatsapp", "WhatsApp"
    EMAIL = "email", "Email"
    VISITA = "visita", "Visita"
    REUNIAO = "reuniao", "Reuniao"
    SUPORTE = "suporte", "Suporte"
    POS_VENDA = "pos_venda", "Pos-venda"


class StatusInteracaoCRM(models.TextChoices):
    ABERTO = "aberto", "Aberto"
    EM_ANDAMENTO = "em_andamento", "Em andamento"
    FINALIZADO = "finalizado", "Finalizado"


class TipoHistoricoRelacionamento(models.TextChoices):
    CRIACAO = "criacao", "Criacao"
    ALTERACAO = "alteracao", "Alteracao"
    BLOQUEIO = "bloqueio", "Bloqueio"
    INATIVACAO = "inativacao", "Inativacao"
    INTERACAO = "interacao", "Interacao"
    ORCAMENTO = "orcamento", "Orcamento"
    ORDEM_SERVICO = "ordem_servico", "Ordem de servico"
    COMPRA = "compra", "Compra"
    NFE = "nfe", "NFe"
    DOCUMENTO = "documento", "Documento"
