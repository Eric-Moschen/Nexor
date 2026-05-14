from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.clientes.enums import StatusRelacionamento, TipoHistoricoRelacionamento
from apps.clientes.services import _criar_relacionamentos, _registrar_historico
from apps.fornecedores.models import Fornecedor
from apps.fornecedores.validators import normalize_documento, validate_documento, validate_email, validate_ie, validate_required_name


def _validar_dados_fornecedor(dados, instance=None):
    validate_required_name(dados.get("razao_social") or getattr(instance, "razao_social", ""))
    documento = normalize_documento(dados.get("documento") or getattr(instance, "documento", ""))
    validate_documento(documento)
    if dados.get("email"):
        validate_email(dados["email"])
    if dados.get("inscricao_estadual"):
        validate_ie(dados["inscricao_estadual"], dados.get("uf", "SP"))
    duplicado = Fornecedor.objects.filter(documento=documento, is_active=True)
    if instance:
        duplicado = duplicado.exclude(pk=instance.pk)
    if duplicado.exists():
        raise ValidationError({"documento": "Ja existe fornecedor ativo com este CPF/CNPJ."})
    dados["documento"] = documento


@transaction.atomic
def criar_fornecedor(*, usuario=None, enderecos=None, contatos=None, **dados):
    _validar_dados_fornecedor(dados)
    usuario_responsavel = dados.pop("usuario_responsavel", None) or usuario
    fornecedor = Fornecedor.objects.create(
        created_by=usuario,
        updated_by=usuario,
        usuario_responsavel=usuario_responsavel,
        **dados,
    )
    _criar_relacionamentos(fornecedor=fornecedor, enderecos=enderecos, contatos=contatos, usuario=usuario)
    _registrar_historico(
        fornecedor=fornecedor,
        tipo_evento=TipoHistoricoRelacionamento.CRIACAO,
        descricao="Fornecedor criado no cadastro central de relacionamento.",
        usuario=usuario,
    )
    return fornecedor


@transaction.atomic
def atualizar_fornecedor(*, fornecedor, usuario=None, enderecos=None, contatos=None, **dados):
    _validar_dados_fornecedor(dados, instance=fornecedor)
    for campo, valor in dados.items():
        setattr(fornecedor, campo, valor)
    fornecedor.updated_by = usuario
    fornecedor.save()
    if enderecos is not None:
        fornecedor.enderecos.update(is_active=False, deleted_at=timezone.now(), updated_by=usuario)
        _criar_relacionamentos(fornecedor=fornecedor, enderecos=enderecos, usuario=usuario)
    if contatos is not None:
        fornecedor.contatos.update(is_active=False, deleted_at=timezone.now(), updated_by=usuario)
        _criar_relacionamentos(fornecedor=fornecedor, contatos=contatos, usuario=usuario)
    _registrar_historico(
        fornecedor=fornecedor,
        tipo_evento=TipoHistoricoRelacionamento.ALTERACAO,
        descricao="Fornecedor atualizado no cadastro central de relacionamento.",
        usuario=usuario,
    )
    return fornecedor


@transaction.atomic
def inativar_fornecedor(*, fornecedor, usuario=None, motivo="Fornecedor inativado."):
    fornecedor.status = StatusRelacionamento.INATIVO
    fornecedor.is_active = False
    fornecedor.deleted_at = timezone.now()
    fornecedor.updated_by = usuario
    fornecedor.save(update_fields=["status", "is_active", "deleted_at", "updated_by", "updated_at"])
    _registrar_historico(fornecedor=fornecedor, tipo_evento=TipoHistoricoRelacionamento.INATIVACAO, descricao=motivo, usuario=usuario)
    return fornecedor
