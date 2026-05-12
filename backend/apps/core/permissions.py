"""Shared permission primitives for future RBAC policies."""
from rest_framework.permissions import BasePermission


class HasRolePermission(BasePermission):
    required_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        user_roles = getattr(request.user, "roles", [])
        return any(role in user_roles for role in self.required_roles)
