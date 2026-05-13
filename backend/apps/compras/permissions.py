from apps.core.permissions import HasModulePermission


class CanManageCompras(HasModulePermission):
    required_permission = "compras.change_comprasrecord"
