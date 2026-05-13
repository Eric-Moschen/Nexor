from apps.core.permissions import HasModulePermission


class CanViewOrcamento(HasModulePermission):
    allowed_roles = {"administrador", "comercial", "supervisor", "financeiro", "operacional"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles


class CanManageOrcamento(CanViewOrcamento):
    allowed_roles = {"administrador", "comercial", "supervisor"}


class CanApproveOrcamento(CanViewOrcamento):
    allowed_roles = {"administrador", "supervisor", "comercial"}
