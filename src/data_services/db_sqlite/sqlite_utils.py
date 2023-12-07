class SQL_Utils:
    def __init__(self, db) -> None:
        self.db = db
    
    def add_new_user(self, username, name, email_id, pwd, dp_url):
        pass
    
    def load_user(self, user_id):
        pass
    
    def get_user(self, username):
        pass
    
    def validate_pwd(self, username, pwd):
        pass
    
    # Group Functions
    def add_new_group(self, groupname, name, member, admins):
        pass
    
    # OnlineUsers Functions
    def add_to_online_user(self, username, session_id):
        pass
    
    def remove_from_online_user(self, username):
        pass
    
    def get_session_id(self, username):
        pass
    
    # UserMessages Functions
    def new_user_message(self, sender, receiver, text):
        pass
    
    def new_user_message_image(self, sender, receiver, url):
        pass
    
    # chunk_num >= 1
    def get_next_set_of_user_messages(self, chunk_num, username1, username2):
        pass

    def add_new_group_message(self, groupname, sender, text):
        pass
    
    def get_next_set_of_group_messages(self, chunk_num, groupname):
        pass