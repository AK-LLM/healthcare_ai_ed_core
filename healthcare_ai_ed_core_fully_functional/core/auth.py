
class User:
    def __init__(self, username="demo_user", role="tester"):
        self.username = username
        self.role = role
    def is_admin(self):
        return self.role == "admin"
    def is_tester(self):
        return self.role == "tester"
def get_current_user():
    return User()
