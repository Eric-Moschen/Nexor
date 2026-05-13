from django.core.exceptions import ValidationError


def validate_required_text(value, field_name="Campo"):
    if not value or not value.strip():
        raise ValidationError(f"{field_name} e obrigatorio.")


def validate_positive_decimal(value, message="Valor deve ser maior que zero."):
    if value <= 0:
        raise ValidationError(message)


def validate_non_negative_decimal(value, message="Valor nao pode ser negativo."):
    if value < 0:
        raise ValidationError(message)
