from apps.core.permissions import HasModulePermission


class CanManageRelatorios(HasModulePermission):
    required_permission = "relatorios.change_relatoriosrecord"
