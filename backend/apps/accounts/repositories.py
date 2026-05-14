from apps.accounts.models import Role, User


class UserRepository:
    def get_for_update(self, user_id):
        return User.objects.select_for_update().get(id=user_id)


class RoleRepository:
    def get_for_update(self, role_id):
        return Role.objects.select_for_update().get(id=role_id, is_active=True)
