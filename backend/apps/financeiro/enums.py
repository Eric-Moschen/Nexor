from django.db import models


class TipoFinanceiro(models.TextChoices):
    RECEITA = "receita", "Receita"
    DESPESA = "despesa", "Despesa"


class StatusContaPagar(models.TextChoices):
    PENDENTE = "pendente", "Pendente"
    PARCIAL = "parcialmente_pago", "Parcialmente pago"
    PAGO = "pago", "Pago"
    VENCIDO = "vencido", "Vencido"
    CANCELADO = "cancelado", "Cancelado"


class StatusContaReceber(models.TextChoices):
    PENDENTE = "pendente", "Pendente"
    PARCIAL = "parcialmente_recebido", "Parcialmente recebido"
    RECEBIDO = "recebido", "Recebido"
    VENCIDO = "vencido", "Vencido"
    CANCELADO = "cancelado", "Cancelado"


class TipoBaixa(models.TextChoices):
    PAGAMENTO = "pagamento", "Pagamento"
    RECEBIMENTO = "recebimento", "Recebimento"
