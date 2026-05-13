from django.core.exceptions import ValidationError


def validate_positive_quantity(value):
    if value <= 0:
        raise ValidationError("A quantidade deve ser maior que zero.")


def validate_non_negative_money(value):
    if value < 0:
        raise ValidationError("Valor nao pode ser negativo.")
