from apps.clientes.permissions import CanManageRelacionamento, CanViewRelacionamento


class CanViewFornecedores(CanViewRelacionamento):
    pass


class CanManageFornecedores(CanManageRelacionamento):
    allowed_roles = {"administrador", "compras", "supervisor"}
