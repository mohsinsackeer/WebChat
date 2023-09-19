from flask_login import UserMixin

class ChatUser(UserMixin):
    def __init__(self, user):
        self.user = user
        self.username = user['username']
    def get_id(self):
        return self.username
    def __str__(self):
        print(f'User Dict: {self.user}\nis_authenticated: {self.is_authenticated}')