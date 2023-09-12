import pymongo
import time

class MongoAppDB:
    """
    AppDB uses all the 3 databases, and can perform all the database 
    operations of the application.
    """
    def __init__(self, host='localhost', port=27017) -> None:
        CONN_STRING = 'mongo://' + host.strip('/') + '/' + str(port) + '/'
        DB_NAME = "app-db"
        COLLECTION_USERS_NAME = "Users"
        COLLECTION_GROUPS_NAME = "Groups"
        COLLECTION_ONLINE_USERS_NAME = "OnlineUsers"
        COLLECTION_USER_MESSAGES_NAME = "UserMessages"
        COLLECTION_GROUP_MESSAGES_NAME = "GroupMessages"
        
        self.client = pymongo.MongoClient(CONN_STRING)
        self.db_app = self.client[DB_NAME]
        
        # Collection objects for the various DB collections
        self.coll_users = self.db_app[COLLECTION_USERS_NAME]
        self.coll_groups = self.db_app[COLLECTION_GROUPS_NAME]
        self.coll_online_users = self.db_app[COLLECTION_ONLINE_USERS_NAME]
        self.coll_user_messages = self.db_app[COLLECTION_USER_MESSAGES_NAME]
        self.coll_group_messages = self.db_app[COLLECTION_GROUP_MESSAGES_NAME]
    
    def insert_one(self, collection, record):
        collection.insert_one(record)
    
    def find_one(self, collection, filter):
        return collection.find_one(filter)

    """
    Functions for 'Users' Collection
    """
    def add_new_user(self, username, name, email_id, pwd, dp_url):
        user = {
            'username'  : username,
            'name'      : name,
            'email_id'  : email_id,
            'pwd'       : pwd,
            'dp_url'    : dp_url,
            'chats'     : []
        }
        self.coll_users.insert_one(user)
    
    # For Flask Login Manager
    def load_user(self, user_id):
        return self.coll_users.find_one({'_id': user_id})
    
    def get_user(self, username):
        return self.coll_users.find_one({'username': username})
    
    def validate_pwd(self, username, pwd):
        user = self.coll_users.find_one({'username': username}, {'pwd': 1})
        if user:
            return pwd == user['pwd']
        return False

    """
    Functions for 'Groups' Collection
    """
    def add_new_group(self, groupname, name, member, admins):
        group = {
            'groupname'     : groupname,
            'name'          : name,
            'members'       : [],
        }
        for username in member:
            if username in admins:
                group['members'].append({'username': username, 'is_admin': True})
            else:
                group['members'].append({'username': username, 'is_admin': False})
        self.coll_groups.insert_one(group)
    
    """
    Functions for 'OnlineUsers' Collection
    """
    def add_to_online_user(self, username, session_id):
        self.coll_online_users.insert_one({'username': username, 'session_id': session_id})
        print(f'{username} add to OnlineUsers collection')
    
    def remove_from_online_user(self, username):
        self.coll_online_users.delete_one({'username': username})
        print(f'{username} removed from OnlineUsers collection')
    
    def get_session_id(self, username):
        user = self.coll_online_users.find_one({'username': username})
        return user['session_id']
    
    """
    Functions for 'UserMessages' Collection
    """
    def new_user_message(self, sender, receiver, text):
        message = {
            'unique_chat_code': min(sender, receiver) + '-' + max(sender,receiver),
            'from': sender,
            'to': receiver,
            'is_image': False,
            'text': text,
            'timestamp': time.time()
        }
        self.coll_user_messages.insert_one(message)
    
    def new_user_message_image(self, sender, receiver, url):
        message = {
            'unique_chat_code': min(sender, receiver) + '-' + max(sender,receiver),
            'from': sender,
            'to': receiver,
            'is_image': True,
            'text': url,
            'timestamp': time.time()
        }
        self.coll_user_messages.insert_one(message)
    
    def get_next_set_of_user_messages(self, chunk_num, username1, username2):
        unique_chat_code = min(username1,username2) + '-' + max(username1, username2)
        messages = self.coll_user_messages.find({'unique_chat_code': unique_chat_code})\
                                          .sort({'timestamp': -1})\
                                          .skip((chunk_num-1)*100)\
                                          .limit(100)\
                                          .reverse()
        return messages
    
    """
    Functions for 'GroupMessages' Collection
    """
    def add_new_group_message(self, groupname, sender, text):
        message = {
            'groupname' : groupname,
            'from'      : sender,
            'text'      : text,
            'timestamp' : time.time()
        }
        self.coll_group_messages.insert_one(message)

    def get_next_of_group_messages(self, chunk_num, groupname):
        messages = self.coll_group_messages.find({'groupname': groupname})\
                                            .sort({'timestamp': -1})\
                                            .skip((chunk_num-1)*100)\
                                            .limit(100)\
                                            .reverse()
        return messages