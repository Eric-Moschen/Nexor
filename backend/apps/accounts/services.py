from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import AuthAuditLog, Permission, Role, RolePermission, User, UserRole
from apps.accounts.validators import split_permission_code, validate_unique_email, validate_unique_username


def get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    return forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")


def registrar_auditoria(*, request=None, user=None, event, success=True, username_attempted="", metadata=None):
    return AuthAuditLog.objects.create(
        user=user,
        event=event,
        success=success,
        username_attempted=username_attempted,
        ip_address=get_client_ip(request) if request else None,
        user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
        metadata=metadata or {},
    )


@transaction.atomic
def criar_usuario(*, usuario_criador=None, password=None, **dados):
    validate_unique_email(dados["email"])
    validate_unique_username(dados["username"])
    role_code = dados.get("role", User.Role.OPERACIONAL)
    user = User.objects.create_user(password=password or dados.pop("password", None), **dados)
    vincular_perfil(user=user, role_code=role_code, primary=True)
    return user


@transaction.atomic
def atualizar_usuario(*, user, **dados):
    if "email" in dados:
        validate_unique_email(dados["email"], user=user)
    if "username" in dados:
        validate_unique_username(dados["username"], user=user)
    password = dados.pop("password", None)
    role_code = dados.get("role")
    for campo, valor in dados.items():
        setattr(user, campo, valor)
    if password:
        user.set_password(password)
    user.save()
    if role_code:
        vincular_perfil(user=user, role_code=role_code, primary=True)
    return user


@transaction.atomic
def inativar_usuario(*, user):
    user.is_active = False
    user.save(update_fields=["is_active"])
    return user


@transaction.atomic
def ativar_usuario(*, user):
    user.is_active = True
    user.save(update_fields=["is_active"])
    return user


@transaction.atomic
def alterar_senha(*, user, current_password, new_password, request=None):
    if not user.check_password(current_password):
        registrar_auditoria(request=request, user=user, event=AuthAuditLog.Event.PASSWORD_CHANGE, success=False)
        raise ValidationError("Senha atual invalida.")
    user.set_password(new_password)
    user.save(update_fields=["password"])
    registrar_auditoria(request=request, user=user, event=AuthAuditLog.Event.PASSWORD_CHANGE, success=True)
    return user


def login_usuario(*, request, username, password):
    user = authenticate(request=request, username=username, password=password)
    if not user or not user.is_active:
        registrar_auditoria(request=request, user=user, event=AuthAuditLog.Event.LOGIN_FAILED, success=False, username_attempted=username)
        raise ValidationError("Credenciais invalidas.")
    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    refresh = RefreshToken.for_user(user)
    registrar_auditoria(request=request, user=user, event=AuthAuditLog.Event.LOGIN_SUCCESS, success=True)
    return {"access": str(refresh.access_token), "refresh": str(refresh), "user": user}


def logout_usuario(*, request, refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()
    registrar_auditoria(request=request, user=request.user if request and request.user.is_authenticated else None, event=AuthAuditLog.Event.LOGOUT, success=True)


def refresh_usuario(*, refresh_token):
    refresh = RefreshToken(refresh_token)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def verificar_permissao(user, permission_code):
    return user.has_rbac_permission(permission_code)


@transaction.atomic
def salvar_permissoes_role(*, role, permission_codes):
    permissions = []
    for code in permission_codes:
        module, action = split_permission_code(code)
        permission, _ = Permission.objects.get_or_create(code=code, defaults={"module": module, "action": action, "description": code})
        permissions.append(permission)
    RolePermission.objects.filter(role=role).delete()
    RolePermission.objects.bulk_create([RolePermission(role=role, permission=permission) for permission in permissions], ignore_conflicts=True)
    return role


@transaction.atomic
def vincular_perfil(*, user, role_code, primary=False):
    role, _ = Role.objects.get_or_create(code=role_code, defaults={"name": role_code.replace("_", " ").title()})
    membership, _ = UserRole.objects.get_or_create(user=user, role=role, defaults={"is_primary": primary})
    if primary:
        UserRole.objects.filter(user=user).exclude(id=membership.id).update(is_primary=False)
        membership.is_primary = True
        membership.save(update_fields=["is_primary"])
    return membership


def remover_perfil(*, user, role_code):
    UserRole.objects.filter(user=user, role__code=role_code).delete()
