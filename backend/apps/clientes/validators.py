import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.fiscal.validators import only_digits, validate_cep as fiscal_validate_cep, validate_cpf_cnpj


def normalize_documento(value):
    return only_digits(value)


def validate_documento(value):
    validate_cpf_cnpj(value)


def validate_ie(value, uf=""):
    if not value:
        return
    cleaned = re.sub(r"[^0-9A-Za-z]", "", value)
    if len(cleaned) < 2 or len(cleaned) > 14:
        raise ValidationError("Inscricao estadual invalida para a UF informada.")


def validate_cep(value):
    fiscal_validate_cep(value)


def validate_email(value):
    if not value:
        return
    try:
        django_validate_email(value)
    except DjangoValidationError as exc:
        raise ValidationError("Email invalido.") from exc


def validate_required_name(value, label="Nome"):
    if not value or not value.strip():
        raise ValidationError(f"{label} e obrigatorio.")
