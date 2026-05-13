from apps.core.permissions import HasModulePermission


class CanManageFinanceiro(HasModulePermission):
    required_permission = "financeiro.change_financeirorecord"
