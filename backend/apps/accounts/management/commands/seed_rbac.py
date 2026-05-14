from django.core.management.base import BaseCommand

from apps.accounts.enums import DEFAULT_PERMISSIONS, DEFAULT_ROLES
from apps.accounts.models import Permission, Role, RolePermission, User
from apps.accounts.services import vincular_perfil
from apps.accounts.validators import split_permission_code


class Command(BaseCommand):
    help = "Cria perfis, permissoes padrao e usuario admin inicial do Nexor ERP."

    def add_arguments(self, parser):
        parser.add_argument("--admin-email", default="admin@nexor.local")
        parser.add_argument("--admin-username", default="admin")
        parser.add_argument("--admin-password", default="Admin@12345")

    def handle(self, *args, **options):
        permissions = []
        for code in DEFAULT_PERMISSIONS:
            module, action = split_permission_code(code)
            permission, _ = Permission.objects.update_or_create(
                code=code,
                defaults={"module": module, "action": action, "description": code, "is_active": True},
            )
            permissions.append(permission)

        role_map = {}
        for code, name in DEFAULT_ROLES:
            role, _ = Role.objects.update_or_create(code=code, defaults={"name": name, "is_system": True, "is_active": True})
            role_map[code] = role

        admin_role = role_map["administrador"]
        RolePermission.objects.bulk_create([RolePermission(role=admin_role, permission=permission) for permission in permissions], ignore_conflicts=True)

        supervisor_role = role_map["supervisor"]
        RolePermission.objects.bulk_create([RolePermission(role=supervisor_role, permission=permission) for permission in permissions if not permission.code.startswith("accounts.")], ignore_conflicts=True)

        admin, created = User.objects.get_or_create(
            username=options["admin_username"],
            defaults={
                "email": options["admin_email"],
                "first_name": "Admin",
                "role": User.Role.ADMINISTRADOR,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password(options["admin_password"])
            admin.save()
        vincular_perfil(user=admin, role_code=User.Role.ADMINISTRADOR, primary=True)
        self.stdout.write(self.style.SUCCESS("RBAC inicial criado com sucesso."))
