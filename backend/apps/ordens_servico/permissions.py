from apps.core.permissions import HasModulePermission


class CanManageOrdensServico(HasModulePermission):
    required_permission = "ordens_servico.change_ordensservicorecord"
