import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIRequestFactory

from apps.accounts.models import Permission, Role, RolePermission, User
from apps.accounts.services import alterar_senha, criar_usuario, login_usuario, salvar_permissoes_role, verificar_permissao


@pytest.fixture
def role(db):
    return Role.objects.create(code="financeiro", name="Financeiro")


@pytest.fixture
def usuario(db, role):
    user = criar_usuario(username="financeiro", email="financeiro@nexor.test", password="test12345", role="financeiro")
    salvar_permissoes_role(role=role, permission_codes=["financeiro.conta_pagar.visualizar"])
    return user


@pytest.mark.django_db
def test_login_valido(usuario):
    request = APIRequestFactory().post("/api/v1/auth/login/")
    result = login_usuario(request=request, username="financeiro", password="test12345")

    assert result["access"]
    assert result["refresh"]


@pytest.mark.django_db
def test_login_invalido_bloqueia():
    request = APIRequestFactory().post("/api/v1/auth/login/")

    with pytest.raises(ValidationError):
        login_usuario(request=request, username="inexistente", password="errada")


@pytest.mark.django_db
def test_usuario_inativo_nao_loga(usuario):
    usuario.is_active = False
    usuario.save(update_fields=["is_active"])
    request = APIRequestFactory().post("/api/v1/auth/login/")

    with pytest.raises(ValidationError):
        login_usuario(request=request, username="financeiro", password="test12345")


@pytest.mark.django_db
def test_rbac_permite_e_bloqueia(usuario):
    assert verificar_permissao(usuario, "financeiro.conta_pagar.visualizar") is True
    assert verificar_permissao(usuario, "fiscal.nfe.emitir") is False


@pytest.mark.django_db
def test_administrador_acessa_tudo():
    admin = User.objects.create_user(username="admin-rbac", email="admin@nexor.test", password="test12345", role=User.Role.ADMINISTRADOR)

    assert verificar_permissao(admin, "permissao.inexistente.bloqueada") is True


@pytest.mark.django_db
def test_criar_usuario_bloqueia_email_duplicado(usuario):
    with pytest.raises(ValidationError):
        criar_usuario(username="outro", email="financeiro@nexor.test", password="test12345", role="financeiro")


@pytest.mark.django_db
def test_alterar_senha(usuario):
    request = APIRequestFactory().post("/api/v1/auth/change-password/")
    alterar_senha(user=usuario, request=request, current_password="test12345", new_password="novaSenha123")
    usuario.refresh_from_db()

    assert usuario.check_password("novaSenha123")
