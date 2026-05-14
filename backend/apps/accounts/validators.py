from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email

from apps.accounts.models import User


def validate_unique_email(email, user=None):
    try:
        django_validate_email(email)
    except ValidationError as exc:
        raise ValidationError("Email invalido.") from exc
    queryset = User.objects.filter(email__iexact=email)
    if user:
        queryset = queryset.exclude(pk=user.pk)
    if queryset.exists():
        raise ValidationError("Email ja cadastrado.")


def validate_unique_username(username, user=None):
    queryset = User.objects.filter(username__iexact=username)
    if user:
        queryset = queryset.exclude(pk=user.pk)
    if queryset.exists():
        raise ValidationError("Username ja cadastrado.")


def split_permission_code(code):
    parts = code.split(".")
    if len(parts) < 3:
        raise ValidationError("Permissao deve seguir o padrao modulo.recurso.acao.")
    return parts[0], parts[-1]
