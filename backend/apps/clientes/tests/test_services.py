from datetime import timedelta

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.accounts.models import User
from apps.clientes.enums import StatusInteracaoCRM, StatusRelacionamento, TipoInteracaoCRM
from apps.clientes.models import HistoricoRelacionamento
from apps.clientes.services import criar_cliente, finalizar_interacao, inativar_cliente, registrar_interacao


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="comercial-crm", password="test12345", role=User.Role.COMERCIAL)


@pytest.mark.django_db
def test_criar_cliente_valido_com_endereco_e_contato(usuario):
    cliente = criar_cliente(
        usuario=usuario,
        razao_social="Cliente Relacionamento",
        documento="12.345.678/0001-95",
        email="cliente@nexor.test",
        enderecos=[{"cep": "01001000", "rua": "Rua Central", "numero": "100", "bairro": "Centro", "cidade": "Sao Paulo", "uf": "SP"}],
        contatos=[{"nome": "Maria Cliente", "email": "maria@nexor.test", "principal": True}],
    )

    assert cliente.documento == "12345678000195"
    assert cliente.enderecos.count() == 1
    assert cliente.contatos.count() == 1
    assert HistoricoRelacionamento.objects.filter(cliente=cliente, tipo_evento="criacao").exists()


@pytest.mark.django_db
def test_bloquear_cliente_com_cpf_invalido(usuario):
    with pytest.raises(ValidationError):
        criar_cliente(usuario=usuario, razao_social="CPF invalido", documento="11111111111")


@pytest.mark.django_db
def test_bloquear_cliente_com_cnpj_invalido(usuario):
    with pytest.raises(ValidationError):
        criar_cliente(usuario=usuario, razao_social="CNPJ invalido", documento="11111111000111")


@pytest.mark.django_db
def test_bloquear_duplicidade_de_documento_ativo(usuario):
    criar_cliente(usuario=usuario, razao_social="Cliente A", documento="12345678000195")

    with pytest.raises(ValidationError):
        criar_cliente(usuario=usuario, razao_social="Cliente B", documento="12345678000195")


@pytest.mark.django_db
def test_inativar_cliente_preserva_historico(usuario):
    cliente = criar_cliente(usuario=usuario, razao_social="Cliente Inativar", documento="52998224725")

    inativar_cliente(cliente=cliente, usuario=usuario)
    cliente.refresh_from_db()

    assert cliente.is_active is False
    assert cliente.status == StatusRelacionamento.INATIVO
    assert HistoricoRelacionamento.objects.filter(cliente=cliente, tipo_evento="inativacao").exists()


@pytest.mark.django_db
def test_registrar_e_finalizar_interacao_crm(usuario):
    cliente = criar_cliente(usuario=usuario, razao_social="Cliente CRM", documento="12345678000195")
    interacao = registrar_interacao(
        cliente=cliente,
        usuario=usuario,
        tipo_interacao=TipoInteracaoCRM.LIGACAO,
        descricao="Contato sobre proposta",
        data=timezone.now(),
        proximo_contato=timezone.now() + timedelta(days=2),
    )

    finalizar_interacao(interacao=interacao, usuario=usuario)
    interacao.refresh_from_db()

    assert interacao.status == StatusInteracaoCRM.FINALIZADO
    assert HistoricoRelacionamento.objects.filter(cliente=cliente, tipo_evento="interacao").count() == 2
