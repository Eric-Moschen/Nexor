from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_data_validade(value):
    if value < timezone.localdate():
        raise ValidationError("Data de validade nao pode ser anterior a data atual.")


def validate_positive(value, message="Valor deve ser maior que zero."):
    if value <= 0:
        raise ValidationError(message)


def validate_non_negative(value, message="Valor nao pode ser negativo."):
    if value < 0:
        raise ValidationError(message)
