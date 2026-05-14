from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import AuthAuditLog, LoginAudit, Permission, Role, RolePermission, User, UserRole


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Nexor ERP", {"fields": ("role", "telefone", "cargo")}),)
    list_display = ("username", "email", "role", "cargo", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")


@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "success", "created_at")
    list_filter = ("success", "created_at")


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_system", "is_active")
    list_filter = ("is_system", "is_active")
    search_fields = ("code", "name")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "module", "action", "is_active")
    list_filter = ("module", "action", "is_active")
    search_fields = ("code", "description")


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "permission", "created_at")
    search_fields = ("role__code", "permission__code")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_primary", "created_at")
    list_filter = ("role", "is_primary")


@admin.register(AuthAuditLog)
class AuthAuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "success", "ip_address", "created_at")
    list_filter = ("event", "success", "created_at")
    search_fields = ("user__username", "username_attempted", "ip_address")
