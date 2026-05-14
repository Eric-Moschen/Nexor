from django.db import models


class CategoriaFornecedor(models.TextChoices):
    MATERIA_PRIMA = "materia_prima", "Materia-prima"
    FERRAMENTAS = "ferramentas", "Ferramentas"
    SERVICOS = "servicos", "Servicos"
    TRANSPORTE = "transporte", "Transporte"
    TERCEIRIZADOS = "terceirizados", "Terceirizados"
    OUTROS = "outros", "Outros"
