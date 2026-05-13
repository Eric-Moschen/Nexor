from apps.core.permissions import HasModulePermission


class CanManageEstoque(HasModulePermission):
    allowed_roles = {"administrador", "estoque", "compras", "supervisor"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles
