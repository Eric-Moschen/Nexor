from apps.core.permissions import HasModulePermission


class CanViewRelacionamento(HasModulePermission):
    allowed_roles = {"administrador", "comercial", "compras", "financeiro", "operacional", "supervisor"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles


class CanManageRelacionamento(CanViewRelacionamento):
    allowed_roles = {"administrador", "comercial", "compras", "supervisor"}


class CanManageClientes(CanManageRelacionamento):
    allowed_roles = {"administrador", "comercial", "supervisor"}
