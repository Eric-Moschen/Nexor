from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date


def validate_required_name(value):
    if not value or not value.strip():
        raise ValidationError("O nome e obrigatorio.")


def validar_periodo(data_inicial=None, data_final=None):
    inicio = parse_date(data_inicial) if isinstance(data_inicial, str) and data_inicial else data_inicial
    fim = parse_date(data_final) if isinstance(data_final, str) and data_final else data_final
    if data_inicial and inicio is None:
        raise ValidationError("Data inicial invalida.")
    if data_final and fim is None:
        raise ValidationError("Data final invalida.")
    if inicio and fim and inicio > fim:
        raise ValidationError("Data inicial nao pode ser maior que a data final.")
    return inicio, fim


def normalizar_filtros(params):
    filtros = {
        "data_inicial": params.get("data_inicial", ""),
        "data_final": params.get("data_final", ""),
        "cliente": params.get("cliente", ""),
        "fornecedor": params.get("fornecedor", ""),
        "status": params.get("status", ""),
        "centro_custo": params.get("centro_custo", ""),
        "categoria": params.get("categoria", ""),
        "responsavel": params.get("responsavel", ""),
        "tipo_operacao": params.get("tipo_operacao", ""),
    }
    validar_periodo(filtros["data_inicial"], filtros["data_final"])
    return {chave: valor for chave, valor in filtros.items() if valor not in ("", None)}
