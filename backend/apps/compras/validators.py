from django.core.exceptions import ValidationError


def validate_required_name(value):
    if not value or not value.strip():
        raise ValidationError("O nome e obrigatorio.")
