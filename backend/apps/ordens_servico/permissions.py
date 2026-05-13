from apps.core.permissions import HasModulePermission


class CanViewOrdensServico(HasModulePermission):
    allowed_roles = {"administrador", "operacional", "supervisor", "estoque", "financeiro", "fiscal"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles


class CanManageOrdensServico(CanViewOrdensServico):
    allowed_roles = {"administrador", "operacional", "supervisor"}


class CanApproveOrdensServico(CanViewOrdensServico):
    allowed_roles = {"administrador", "supervisor"}


class CanBillOrdensServico(CanViewOrdensServico):
    allowed_roles = {"administrador", "financeiro", "supervisor"}
