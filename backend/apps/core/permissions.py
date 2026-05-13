from rest_framework.permissions import BasePermission


class HasModulePermission(BasePermission):
    required_permission = None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        permission = getattr(view, "required_permission", self.required_permission)
        return True if permission is None else request.user.has_perm(permission)
