def assign_role(user, role):
    user.role = role
    user.save(update_fields=["role"])
    return user
