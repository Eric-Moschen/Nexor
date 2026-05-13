from apps.core.permissions import HasModulePermission


class CanManageFiscal(HasModulePermission):
    required_permission = "fiscal.change_fiscalrecord"
