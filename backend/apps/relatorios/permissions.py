from apps.core.permissions import HasModulePermission


class CanViewAnalytics(HasModulePermission):
    allowed_roles = {"administrador", "diretoria", "financeiro", "comercial", "operacional", "supervisor"}

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        if request.user.is_superuser:
            return True
        return getattr(request.user, "role", None) in self.allowed_roles


class CanViewFinancialAnalytics(CanViewAnalytics):
    allowed_roles = {"administrador", "diretoria", "financeiro", "supervisor"}


class CanViewCommercialAnalytics(CanViewAnalytics):
    allowed_roles = {"administrador", "diretoria", "comercial", "supervisor"}


class CanViewOperationalAnalytics(CanViewAnalytics):
    allowed_roles = {"administrador", "diretoria", "operacional", "supervisor"}


class CanManageRelatorios(CanViewAnalytics):
    allowed_roles = {"administrador", "diretoria", "financeiro", "supervisor"}
