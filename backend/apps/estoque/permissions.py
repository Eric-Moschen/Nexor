from apps.core.permissions import HasModulePermission


class CanManageEstoque(HasModulePermission):
    required_permission = "estoque.change_estoquerecord"
