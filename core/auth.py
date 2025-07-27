class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

def get_current_user():
    # For demo: returns a hardcoded admin user
    return User("admin", "Administrator")
