from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.clientes.enums import StatusInteracaoCRM, StatusRelacionamento, TipoHistoricoRelacionamento
from apps.clientes.models import Cliente, ContatoRelacionamento, EnderecoRelacionamento, HistoricoRelacionamento, InteracaoCRM
from apps.clientes.validators import normalize_documento, validate_cep, validate_documento, validate_email, validate_ie, validate_required_name


def _registrar_historico(*, cliente=None, fornecedor=None, tipo_evento, descricao, usuario=None, dados_extras=None):
    return HistoricoRelacionamento.objects.create(
        cliente=cliente,
        fornecedor=fornecedor,
        tipo_evento=tipo_evento,
        descricao=descricao,
        usuario_responsavel=usuario,
        dados_extras=dados_extras or {},
    )


def _validar_dados_cliente(dados, instance=None):
    validate_required_name(dados.get("razao_social") or getattr(instance, "razao_social", ""))
    documento = normalize_documento(dados.get("documento") or getattr(instance, "documento", ""))
    validate_documento(documento)
    if dados.get("email"):
        validate_email(dados["email"])
    if dados.get("inscricao_estadual"):
        validate_ie(dados["inscricao_estadual"], dados.get("uf", "SP"))
    duplicado = Cliente.objects.filter(documento=documento, is_active=True)
    if instance:
        duplicado = duplicado.exclude(pk=instance.pk)
    if duplicado.exists():
        raise ValidationError({"documento": "Ja existe cliente ativo com este CPF/CNPJ."})
    dados["documento"] = documento


def _criar_relacionamentos(*, cliente=None, fornecedor=None, enderecos=None, contatos=None, usuario=None):
    for endereco in enderecos or []:
        validate_cep(endereco.get("cep", ""))
        EnderecoRelacionamento.objects.create(cliente=cliente, fornecedor=fornecedor, created_by=usuario, updated_by=usuario, **endereco)
    for contato in contatos or []:
        if contato.get("email"):
            validate_email(contato["email"])
        ContatoRelacionamento.objects.create(cliente=cliente, fornecedor=fornecedor, created_by=usuario, updated_by=usuario, **contato)


@transaction.atomic
def criar_cliente(*, usuario=None, enderecos=None, contatos=None, **dados):
    _validar_dados_cliente(dados)
    usuario_responsavel = dados.pop("usuario_responsavel", None) or usuario
    cliente = Cliente.objects.create(
        created_by=usuario,
        updated_by=usuario,
        usuario_responsavel=usuario_responsavel,
        **dados,
    )
    _criar_relacionamentos(cliente=cliente, enderecos=enderecos, contatos=contatos, usuario=usuario)
    _registrar_historico(
        cliente=cliente,
        tipo_evento=TipoHistoricoRelacionamento.CRIACAO,
        descricao="Cliente criado no cadastro central de relacionamento.",
        usuario=usuario,
    )
    return cliente


@transaction.atomic
def atualizar_cliente(*, cliente, usuario=None, enderecos=None, contatos=None, **dados):
    _validar_dados_cliente(dados, instance=cliente)
    for campo, valor in dados.items():
        setattr(cliente, campo, valor)
    cliente.updated_by = usuario
    cliente.save()

    if enderecos is not None:
        cliente.enderecos.update(is_active=False, deleted_at=timezone.now(), updated_by=usuario)
        _criar_relacionamentos(cliente=cliente, enderecos=enderecos, usuario=usuario)
    if contatos is not None:
        cliente.contatos.update(is_active=False, deleted_at=timezone.now(), updated_by=usuario)
        _criar_relacionamentos(cliente=cliente, contatos=contatos, usuario=usuario)

    _registrar_historico(
        cliente=cliente,
        tipo_evento=TipoHistoricoRelacionamento.ALTERACAO,
        descricao="Cliente atualizado no cadastro central de relacionamento.",
        usuario=usuario,
    )
    return cliente


@transaction.atomic
def bloquear_cliente(*, cliente, usuario=None, motivo="Cliente bloqueado."):
    cliente.status = StatusRelacionamento.BLOQUEADO
    cliente.updated_by = usuario
    cliente.save(update_fields=["status", "updated_by", "updated_at"])
    _registrar_historico(cliente=cliente, tipo_evento=TipoHistoricoRelacionamento.BLOQUEIO, descricao=motivo, usuario=usuario)
    return cliente


@transaction.atomic
def inativar_cliente(*, cliente, usuario=None, motivo="Cliente inativado."):
    cliente.status = StatusRelacionamento.INATIVO
    cliente.is_active = False
    cliente.deleted_at = timezone.now()
    cliente.updated_by = usuario
    cliente.save(update_fields=["status", "is_active", "deleted_at", "updated_by", "updated_at"])
    _registrar_historico(cliente=cliente, tipo_evento=TipoHistoricoRelacionamento.INATIVACAO, descricao=motivo, usuario=usuario)
    return cliente


@transaction.atomic
def registrar_interacao(*, cliente, usuario=None, **dados):
    responsavel = dados.get("responsavel") or usuario
    if responsavel is None:
        raise ValidationError({"responsavel": "Interacao CRM exige responsavel."})
    dados_criacao = dict(dados)
    dados_criacao.pop("cliente", None)
    dados_criacao.pop("responsavel", None)
    interacao = InteracaoCRM.objects.create(
        cliente=cliente,
        responsavel=responsavel,
        created_by=usuario,
        updated_by=usuario,
        **dados_criacao,
    )
    _registrar_historico(
        cliente=cliente,
        tipo_evento=TipoHistoricoRelacionamento.INTERACAO,
        descricao=f"Interacao CRM registrada: {interacao.tipo_interacao}.",
        usuario=usuario,
        dados_extras={"interacao_id": interacao.id, "status": interacao.status},
    )
    return interacao


@transaction.atomic
def atualizar_interacao(*, interacao, usuario=None, **dados):
    if dados.get("responsavel") is None and interacao.responsavel_id is None:
        raise ValidationError({"responsavel": "Interacao CRM exige responsavel."})
    for campo, valor in dados.items():
        setattr(interacao, campo, valor)
    interacao.updated_by = usuario
    interacao.save()
    _registrar_historico(
        cliente=interacao.cliente,
        tipo_evento=TipoHistoricoRelacionamento.INTERACAO,
        descricao="Interacao CRM atualizada.",
        usuario=usuario,
        dados_extras={"interacao_id": interacao.id, "status": interacao.status},
    )
    return interacao


@transaction.atomic
def finalizar_interacao(*, interacao, usuario=None):
    interacao.status = StatusInteracaoCRM.FINALIZADO
    interacao.updated_by = usuario
    interacao.save(update_fields=["status", "updated_by", "updated_at"])
    _registrar_historico(
        cliente=interacao.cliente,
        tipo_evento=TipoHistoricoRelacionamento.INTERACAO,
        descricao="Interacao CRM finalizada.",
        usuario=usuario,
        dados_extras={"interacao_id": interacao.id, "status": interacao.status},
    )
    return interacao
