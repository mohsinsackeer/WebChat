from flask_login import UserMixin

class ChatUser(UserMixin):
    def __init__(self, user):
        self.user = user
        self.username = user['username']
        self.name = user['name']
        self.email_id = user['email_id']
        self.pwd = user['pwd']
        self.dp_url = user['dp_url']
        self.chats = user['chats']
    def get_id(self):
        return self.username
    def __str__(self):
        print(f'User Dict: {self.user}\nis_authenticated: {self.is_authenticated}')