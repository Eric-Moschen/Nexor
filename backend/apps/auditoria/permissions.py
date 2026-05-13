from apps.core.permissions import HasModulePermission


class CanManageAuditoria(HasModulePermission):
    required_permission = "auditoria.change_auditoriarecord"
