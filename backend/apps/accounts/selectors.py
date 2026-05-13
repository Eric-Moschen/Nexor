from apps.accounts.models import User


def list_active_users():
    return User.objects.filter(is_active=True).order_by("first_name", "username")
