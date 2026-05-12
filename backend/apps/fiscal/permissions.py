"""Domain permissions prepared for RBAC expansion."""
from apps.core.permissions import HasRolePermission


class DomainAccessPermission(HasRolePermission):
    required_roles = []
