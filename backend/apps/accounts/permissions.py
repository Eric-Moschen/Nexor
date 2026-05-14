from rest_framework.permissions import BasePermission


class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or getattr(request.user, "role", "") == "administrador"))


class HasPermission(BasePermission):
    required_permission = None

    def __init__(self, permission_code=None):
        if permission_code is not None:
            self.required_permission = permission_code

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        permission = getattr(view, "required_permission", None) or self.required_permission
        return request.user.has_rbac_permission(permission)


def has_permission(permission_code):
    class PermissionRequired(HasPermission):
        required_permission = permission_code

    return PermissionRequired
