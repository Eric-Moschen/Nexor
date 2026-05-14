from rest_framework import serializers

from apps.accounts.models import AuthAuditLog, Permission, Role, User


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "code", "module", "action", "description", "is_active")
        read_only_fields = ("id",)


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ("id", "code", "name", "description", "is_system", "is_active", "permissions", "created_at", "updated_at")
        read_only_fields = ("id", "is_system", "created_at", "updated_at")

    def get_permissions(self, obj):
        return list(obj.role_permissions.select_related("permission").values_list("permission__code", flat=True))


class RolePermissionUpdateSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.CharField(max_length=120), allow_empty=True)


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    nome_completo = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "nome_completo",
            "telefone",
            "cargo",
            "role",
            "roles",
            "permissions",
            "is_active",
            "is_staff",
            "last_login",
            "date_joined",
        )
        read_only_fields = ("id", "permissions", "roles", "is_staff", "last_login", "date_joined")

    def get_permissions(self, obj):
        if obj.is_superuser or obj.role == User.Role.ADMINISTRADOR:
            return list(Permission.objects.filter(is_active=True).values_list("code", flat=True))
        return list(Permission.objects.filter(roles__role__role_users__user=obj, is_active=True).distinct().values_list("code", flat=True))

    def get_roles(self, obj):
        return list(obj.role_memberships.select_related("role").values_list("role__code", flat=True))


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)


class AuthAuditLogSerializer(serializers.ModelSerializer):
    user_nome = serializers.CharField(source="user.nome_completo", read_only=True)

    class Meta:
        model = AuthAuditLog
        fields = ("id", "user", "user_nome", "event", "ip_address", "user_agent", "username_attempted", "success", "metadata", "created_at")
        read_only_fields = fields
