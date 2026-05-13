import re

from django.core.exceptions import ValidationError


def only_digits(value):
    return re.sub(r"\D", "", value or "")


def validate_cnpj(value):
    digits = only_digits(value)
    if len(digits) != 14 or len(set(digits)) == 1:
        raise ValidationError("CNPJ invalido.")
    weights_first = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights_second = [6, *weights_first]
    if _calculate_digit(digits[:12], weights_first) != int(digits[12]) or _calculate_digit(digits[:13], weights_second) != int(digits[13]):
        raise ValidationError("CNPJ invalido.")


def validate_cpf(value):
    digits = only_digits(value)
    if len(digits) != 11 or len(set(digits)) == 1:
        raise ValidationError("CPF invalido.")
    if _calculate_digit(digits[:9], range(10, 1, -1)) != int(digits[9]) or _calculate_digit(digits[:10], range(11, 1, -1)) != int(digits[10]):
        raise ValidationError("CPF invalido.")


def validate_cpf_cnpj(value):
    digits = only_digits(value)
    if len(digits) == 11:
        return validate_cpf(digits)
    if len(digits) == 14:
        return validate_cnpj(digits)
    raise ValidationError("CPF/CNPJ invalido.")


def validate_cep(value):
    if len(only_digits(value)) != 8:
        raise ValidationError("CEP invalido.")


def validate_ibge(value):
    if len(only_digits(value)) != 7:
        raise ValidationError("Municipio IBGE obrigatorio e deve possuir 7 digitos.")


def validate_ncm(value):
    if len(only_digits(value)) != 8:
        raise ValidationError("NCM obrigatorio e deve possuir 8 digitos.")


def validate_cfop(value):
    if len(only_digits(value)) != 4:
        raise ValidationError("CFOP obrigatorio e deve possuir 4 digitos.")


def _calculate_digit(numbers, weights):
    total = sum(int(number) * weight for number, weight in zip(numbers, weights))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder
