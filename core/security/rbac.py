def has_permission(user, action):
    if user.role == "Administrator":
        return True
    if user.role == "Tester" and action in ("view", "predict"):
        return True
    return False
