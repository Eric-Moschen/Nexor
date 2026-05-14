import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.clientes.enums import StatusRelacionamento
from apps.clientes.models import HistoricoRelacionamento
from apps.fornecedores.enums import CategoriaFornecedor
from apps.fornecedores.services import criar_fornecedor, inativar_fornecedor


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="compras-rel", password="test12345", role=User.Role.COMPRAS)


@pytest.mark.django_db
def test_criar_fornecedor_valido(usuario):
    fornecedor = criar_fornecedor(
        usuario=usuario,
        razao_social="Fornecedor Relacionamento",
        documento="12345678000195",
        categoria=CategoriaFornecedor.MATERIA_PRIMA,
        email="fornecedor@nexor.test",
    )

    assert fornecedor.categoria == CategoriaFornecedor.MATERIA_PRIMA
    assert HistoricoRelacionamento.objects.filter(fornecedor=fornecedor, tipo_evento="criacao").exists()


@pytest.mark.django_db
def test_validar_ie_fornecedor(usuario):
    with pytest.raises(ValidationError):
        criar_fornecedor(usuario=usuario, razao_social="IE invalida", documento="12345678000195", inscricao_estadual="1")


@pytest.mark.django_db
def test_inativar_fornecedor(usuario):
    fornecedor = criar_fornecedor(usuario=usuario, razao_social="Fornecedor Inativar", documento="52998224725")

    inativar_fornecedor(fornecedor=fornecedor, usuario=usuario)
    fornecedor.refresh_from_db()

    assert fornecedor.is_active is False
    assert fornecedor.status == StatusRelacionamento.INATIVO
    assert HistoricoRelacionamento.objects.filter(fornecedor=fornecedor, tipo_evento="inativacao").exists()
