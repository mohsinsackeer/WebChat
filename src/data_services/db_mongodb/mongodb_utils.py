import pymongo
import time
import hashlib

from src.configuration import configs
from cloudinary import uploader
from cloudinary.utils import cloudinary_url

class MongoAppDB:
    
    def __init__(self, host='localhost', port=27017) -> None:
        CONN_STRING = 'mongodb://' + host.strip('/') + '/' + str(port)
        print(f'Conn String: {CONN_STRING}')
        # CONN_STRING = configs.get("MONGODB_DB_STRING").data
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
    def create_new_user(self, username, name, email_id, pwd, dp_url):
        user = {
            'username'  : username,
            'name'      : name,
            'email_id'  : email_id,
            'pwd'       : hashlib.sha256(pwd.encode('UTF-8')).hexdigest(),
            'dp_url'    : dp_url,
            'chats'     : []
        }
        self.coll_users.insert_one(user)
    
    # For Flask Login Manager
    def load_user_by_username(self, username):
        user = self.coll_users.find_one({'username': username})
        if user:
            return user
        return None
    
    def get_user(self, username):
        print(f'Called -> get_user({username})')
        user = self.coll_users.find_one({'username': username})
        print(user)
        return user
    
    def does_user_exist(self, username):
        if self.coll_users.find_one({'username': username}, {'username':1}):
            return True
        return False

    def is_email_already_used(self, email):
        if self.coll_users.find_one({'email': email}, {'username': 1}):
            return True
        return False
    
    def validate_pwd(self, username, pwd):
        user = self.coll_users.find_one({'username': username}, {'pwd': 1})
        print(user)
        if user:
            print(pwd)
            return hashlib.sha256(pwd.encode('UTF-8')).hexdigest() == user['pwd']
        return False

    def remove_user_from_chats(self, chats, username):
        for i,user in enumerate(chats):
            if user['username'] == username:
                chats.pop(i)
                break

    def add_latest_chat_to_list(self, username, chatname, user_type):
        # new_chat = {'chatname': chatname, 'isUser': isUser}
        print(f'Inside add_latest_chat_to_list: {username}, {chatname}, {user_type}')
        new_chat = {}
        if user_type == 'user':
            chat_user = self.coll_users.find_one({'username': chatname})
            new_chat = {
                    'type': 'user',
                    'username': chatname,
                    'name': chat_user['name'],
                    'dp_url': chat_user['dp_url']}
        else:
            chat_group = self.coll_groups.find_one({'groupname': chatname})
            new_chat = {
                'type': 'group',
                'username': chatname,
                'name': chat_group['name'],
                'dp_url': chat_group['dp_url']
            }
        user = self.coll_users.find_one({'username': username})
        self.remove_user_from_chats(user['chats'], chatname)
        user['chats'].append(new_chat)
        # self.coll_users.update_one({'username': username}, user)
        self.coll_users.update_one({'username': username},
                                   {'$set': {'chats': user['chats']}})
    
    def update_user_chat_list(self, sender, receiver, chat_type):
        if chat_type == 'user':
            self.add_latest_chat_to_list(sender, receiver, chat_type)
            self.add_latest_chat_to_list(receiver, sender, chat_type)
        else:
            groupname = receiver
            members = self.get_group_members(groupname)
            for member in members:
                self.add_latest_chat_to_list(member, groupname, chat_type)
    
    def get_list_of_chats(self, username):
        chats = self.coll_users.find_one({'username': username})['chats']
        return chats[::-1]

    """
    Functions for 'Groups' Collection
    """
    def create_new_group(self, groupname, name, dp_url, members, admins):
        group = {
            'groupname'     : groupname,
            'name'          : name,
            'dp_url'        : dp_url,
            'members'       : [],
        }
        for username in members:
            if username in admins:
                group['members'].append({'username': username, 'is_admin': True})
            else:
                group['members'].append({'username': username, 'is_admin': False})
        self.coll_groups.insert_one(group)
    
    def get_group_members(self, groupname):
        group = self.coll_groups.find_one({'groupname': groupname})
        members = group['members']
        return [member['username'] for member in members]
    
    """
    Functions for 'OnlineUsers' Collection
    """
    def add_to_online_users(self, username, session_id):
        self.coll_online_users.insert_one({'username': username, 'session_id': session_id})
        print(f'{username} add to OnlineUsers collection')
    
    def remove_from_online_users(self, username):
        self.coll_online_users.delete_many({'username': username})
        print(f'{username} removed from OnlineUsers collection')
    
    def get_session_id(self, username):
        user = self.coll_online_users.find_one({'username': username})
        if user:
            return user['session_id']
        return None
    
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
        self.update_user_chat_list(sender, receiver, 'user')
    
    def new_user_message_image(self, sender, receiver, base64data):
        upload_result = uploader.upload(base64data)
        url, options = cloudinary_url(
            upload_result['public_id'],
            crop="fill"
        )
        message = {
            'unique_chat_code': min(sender, receiver) + '-' + max(sender,receiver),
            'from': sender,
            'to': receiver,
            'is_image': True,
            'text': url,
            'timestamp': time.time()
        }
        self.coll_user_messages.insert_one(message)
        self.update_user_chat_list(sender, receiver, 'user')
        return url
    
    # chunk_num >= 1
    def get_next_set_of_user_messages(self, chunk_num, username1, username2):
        unique_chat_code = min(username1,username2) + '-' + max(username1, username2)
        messages = self.coll_user_messages.find({'unique_chat_code': unique_chat_code}, {'_id':0})\
                                          .sort('timestamp', -1)\
                                          .skip((chunk_num-1)*100)\
                                          .limit(100)
        return list(messages)[::-1]
    
    """
    Functions for 'GroupMessages' Collection
    """
    def add_new_group_message(self, groupname, sender, text):
        message = {
            'groupname' : groupname,
            'from'      : sender,
            'text'      : f'{sender}: {text}',
            'is_image'  : False,
            'timestamp' : time.time()
        }
        self.coll_group_messages.insert_one(message)
        self.update_user_chat_list(sender, groupname, 'group')
    
    def add_new_group_message_image(self, groupname, sender, url):
        message = {
            'groupname' : groupname,
            'from'      : sender,
            'text'      : url,
            'is_image'  : True,
            'timestamp' : time.time()
        }
        self.coll_group_messages.insert_one(message)
        self.update_user_chat_list(sender, groupname, 'group')

    def get_next_set_of_group_messages(self, chunk_num, groupname):
        messages = self.coll_group_messages.find({'groupname': groupname})\
                                            .sort({'timestamp': -1})\
                                            .skip((chunk_num-1)*100)\
                                            .limit(100)\
                                            .reverse()
        return messages