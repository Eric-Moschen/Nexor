from apps.core.permissions import HasModulePermission


class CanManageClientes(HasModulePermission):
    required_permission = "clientes.change_clientesrecord"
