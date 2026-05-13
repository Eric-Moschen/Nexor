from apps.core.permissions import HasModulePermission


class CanViewCompras(HasModulePermission):
    allowed_roles = {"administrador", "compras", "supervisor", "estoque", "financeiro"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles


class CanManageCompras(CanViewCompras):
    allowed_roles = {"administrador", "compras", "supervisor"}


class CanApproveCompras(CanViewCompras):
    allowed_roles = {"administrador", "supervisor"}


class CanReceiveCompras(CanViewCompras):
    allowed_roles = {"administrador", "compras", "estoque"}
