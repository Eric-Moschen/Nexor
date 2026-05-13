from apps.core.permissions import HasModulePermission


class CanManageFornecedores(HasModulePermission):
    required_permission = "fornecedores.change_fornecedoresrecord"
