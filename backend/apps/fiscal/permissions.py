from apps.core.permissions import HasModulePermission


class CanViewFiscal(HasModulePermission):
    allowed_roles = {"administrador", "fiscal", "financeiro", "estoque", "operacional", "supervisor"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles


class CanManageFiscal(CanViewFiscal):
    allowed_roles = {"administrador", "fiscal", "supervisor"}
