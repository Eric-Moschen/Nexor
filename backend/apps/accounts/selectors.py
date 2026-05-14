from apps.accounts.models import AuthAuditLog, Permission, Role, User


def list_active_users():
    return User.objects.prefetch_related("role_memberships__role").filter(is_active=True).order_by("first_name", "username")


def list_users():
    return User.objects.prefetch_related("role_memberships__role").order_by("first_name", "username")


def list_roles():
    return Role.objects.prefetch_related("role_permissions__permission").filter(is_active=True).order_by("name")


def list_permissions():
    return Permission.objects.filter(is_active=True).order_by("module", "code")


def list_auth_audit():
    return AuthAuditLog.objects.select_related("user").order_by("-created_at", "-id")
