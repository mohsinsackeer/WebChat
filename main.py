import socketio
from src import create_app, User, Messages, Groups, GroupMessages, db, cloudinary_creds
from flask import request, session
from flask_socketio import SocketIO
import flask_login
from sqlalchemy import or_, and_

app = create_app()
app.config['SECRET KEY'] = 'ThisTheIsKeySecret'
app.config['clients'] = {}
socketio = SocketIO(app)

@socketio.on('connect')
def add_client():
    print(f"Event for {flask_login.current_user.username} connect")
    # On connecting, we save the session id for each user
    app.config['clients'][flask_login.current_user.username] = request.sid
    print(f'{flask_login.current_user.username}: {request.sid}')
    
    # We return the JSON object with the current user's (sender's) username
    data_to_send = {
        'sender':   flask_login.current_user.username,
        'dp_url': flask_login.current_user.dp_url
    }
    print(f"{flask_login.current_user.username}: {data_to_send}")
    socketio.emit('set-username', data_to_send, room=app.config['clients'][flask_login.current_user.username])

@socketio.on('req-list-of-contacts')
def send_contacts(data):
    username = flask_login.current_user.username

    print("Event for {username}: req-list-of-contacts")

    # Send the list of users in the database to the website
    # Prepare the list of users
    list_of_users = []

    # To list out the name of all users, uncomment the below code:
    # list_of_users = [{'username':user.username, 'name':user.name} for user in User.query.all()]
    results = db.session.query(Messages).filter(
        or_(Messages.sender.like(username),
            Messages.receiver.like(username))
    ).all()
    for result in results[::-1]:
        if not (result.sender in [usr['username'] for usr in list_of_users] or\
                result.receiver in [usr['username'] for usr in list_of_users]):
            
            if result.sender == username and result.receiver not in list_of_users:
                user = User.query.filter_by(username=result.receiver).all()
            elif result.receiver == username and result.sender not in list_of_users:
                user = User.query.filter_by(username=result.sender).all()
            
            valid_user = {
                'type': 'user',
                'username': user[0].username,
                'name': user[0].name,
                'dp_url': user[0].dp_url}
            if valid_user not in list_of_users:
                list_of_users.append(valid_user)

    # Create list_of_groups the user is present in
    list_of_groups = []
    # Query all the groups in the `Group` database table
    # And add only the groups in which the user's username is present in Groups.members
    all_groups = Groups.query.all()
    # List of all members in the group
    for group in all_groups[::-1]:
        members = group.members.strip(',').split(',')
        if username in members:
            list_of_groups.append({
                'type': 'group',
                'username': group.name,
                'name': group.name,
                'dp_url': group.dp_url
                })
    print(f'list-of-contacts for {username}: {list_of_users + list_of_groups}')
    socketio.emit('get-list-of-contacts',
                list_of_users + list_of_groups,
                room=app.config['clients'][flask_login.current_user.username])
    

@socketio.on('disconnect')
def remove_client():
    print(f"Event for {flask_login.current_user.username}: disconnect")
    print(f"Username: {flask_login.current_user.username}")
    print(app.config['clients'])
    app.config['clients'].pop(flask_login.current_user.username)

@socketio.on('req-list-of-messages')
def get_existing_messages(receiver):
    print(f"Event for {flask_login.current_user.username}: req-list-of-messages of {receiver}")
    sender = flask_login.current_user.username

    if receiver['type'] == 'user':
        receiver = receiver['name_or_username']
        messages = db.session.query(Messages).filter(
            or_(
                and_(
                    Messages.sender.like(sender),
                    Messages.receiver.like(receiver)
                ),
                and_(
                    Messages.sender.like(receiver),
                    Messages.receiver.like(sender)
                )
            )
        )
        list_of_messages = [{'message': message.message, 'class_name': 'sent'}
                            if message.sender == sender
                            else
                            {'message': message.message, 'class_name': 'received'}
                            for message in messages]
    
    else:
        # Query GroupMessages
        list_of_messages = []
        name_of_group = receiver['name_or_username']
        messages = GroupMessages.query.filter_by(group_name=name_of_group)
        for message in messages:
            if message.sender == sender:
                list_of_messages.append({'message': message.message, 'class_name': 'sent'})
            else:
                list_of_messages.append({'message': f'{message.sender}: {message.message}', 'class_name': 'received'})
    
    socketio.emit('get-list-of-messages', list_of_messages, room=app.config['clients'][sender])

@socketio.on('send-message')
def handle_message(data):
    sender = flask_login.current_user.username
    print(f"Event for {sender}: send-message")
    type = data['type']
    name_or_username = data['receiver']
    message = data['message']

    # Save the message to the database
    if type == 'user':
        new_message = Messages()
        new_message.sender = flask_login.current_user.username
        new_message.receiver = name_or_username
        new_message.message = message
        db.session.add(new_message)
        db.session.commit()
        
        data_to_send = {
            'message'   :   message,
            'from'    :   flask_login.current_user.username
        }
        print(f"Data: {data_to_send}")

        if name_or_username in app.config['clients']:
            socketio.emit('display-message', data_to_send, room=app.config['clients'][name_or_username])
    
    else:
        new_message = GroupMessages()
        new_message.group_name = name_or_username
        new_message.sender = flask_login.current_user.username
        new_message.message = message
        db.session.add(new_message)
        db.session.commit()

        data_to_send = {
            'message': f'{sender}: {message}',
            'class_name': 'received'
            }
        print(f"Data: {data_to_send}")
        group_members = Groups\
                        .query\
                        .filter_by(name=name_or_username)[0]\
                        .members.strip(',')\
                        .split(',')
        for member in group_members:
            if member in app.config['clients'] and member!=sender:
                socketio.emit('display-message', data_to_send, room=app.config['clients'][member])

@socketio.on('doesUsernameExists')
def does_username_exists(data):
    user_name = data['username']
    result = User.query.filter_by(username=f'{user_name}').first()
    # result = User.query.filter_by(username='Jogn')
    try:
        if result.username:
            data = {'answer': 'True',
                    'username': result.username,
                    'name': result.name,
                    'dp_url': result.dp_url}
    except Exception as e:
        print(e)
        data = {'answer': 'False'}
    print(data)
    socketio.emit('answerToDoesUsernameExists',
                data,
                room=app.config['clients'][flask_login.current_user.username])

@socketio.on('create-new-group')
def create_new_group(data):
    name = data['name']
    members = data['members']
    admins = data['admins']
    username = flask_login.current_user.username

    members = [member.strip() for member in members.split(',') if isUserExists(member.strip())]
    admins = [admin.strip() for admin in admins.split(',') if isUserExists(admin.strip())]
    # if sender not in members:
    #     members.append(sender)

    """
    Error Cases:
    1. Person who created the group is not in it
    2. Person who created the group is not an admin
    3. If no member in group other than person who created
    4. Usernames in admins not in members
    5. Group size > 15
    """
    flag = True
    # Case 1
    if username not in members:
        members.append(username)
    # Case 2
    if username not in admins:
        admins.append(username)
    # Case 3
    if len(members) == 1:
        warning_or_error = 'Error: Group Creation Failed'
        message = f'You must add at least one more member in the group!'
        show_warning_error(username, warning_or_error, message)
        flag = False
        print("Case 3 Failed")
        return
    print("Case 3 Success")
    # Case 4
    users = []
    for admin in admins:
        if admin not in members:
            users.append(admin)
    users = ', '.join(users)
    if len(users) > 0:
        warning_or_error = 'Error: Group Creation Failed'
        message = f'Given admins: {users} is not mentioned as members!'
        show_warning_error(username, warning_or_error, message)
        flag = False
        print("Case 4 Failed")
        return
    print("Case 4 Success")
    # Case 5
    if len(members) > 15:
        warning_or_error = 'Error: Group Creation Failed'
        message = f'Groups can have max 15 members!'
        show_warning_error(username, warning_or_error, message)
        flag = False
        print("Case 5 Failed")
        return
    print("Case 5 Success")

    if flag:
        members = ",".join(members)
        admins = ",".join(admins)

        group = Groups()
        group.name = name
        group.members = members
        group.admins = admins
        group.dp_url = 'https://png.pngitem.com/pimgs/s/150-1503945_transparent-user-png-default-user-image-png-png.png'
        db.session.add(group)
        db.session.commit()


    socketio.emit('group-created',
                'Success',
                room=app.config['clients'][username])

def isUserExists(username):
    results = User.query.filter_by(username=username).first()
    if results:
        return True
    return False

def show_warning_error(username, title, message):
    data_to_send = {
        'warning_or_error': title,
        'message': message
    }
    socketio.emit('warning-or-error',
                data_to_send,
                room=app.config['clients'][username])

if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, port='8080', host='0.0.0.0')
    # socketio.run(app, debug=True)
