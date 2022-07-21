import socketio
from src import create_app, User, Messages, Groups, GroupMessages, db
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
        'sender'  :   flask_login.current_user.username
    }
    print(f"{flask_login.current_user.username}: {data_to_send}")
    socketio.emit('set-username', data_to_send, room=app.config['clients'][flask_login.current_user.username])

    # Send the list of users in the database to the website
    # Prepare the list of users
    list_of_users = []

    # To list out the name of all users, uncomment the below code:
    # list_of_users = [{'username':user.username, 'name':user.name} for user in User.query.all()]
    username = flask_login.current_user.username
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
                'name': user[0].name}
            if valid_user not in list_of_users:
                list_of_users.append(valid_user)

    # Create list_of_groups the user is present in
    list_of_groups = []
    # Query all the groups in the `Group` database table
    # And add only the groups in which the user's username is present in Groups.members
    all_groups = Groups.query.all()
    # List of all members in the group
    for group in all_groups:
        members = group.members.strip(',').split(',')
        if username in members:
            list_of_groups.append({
                'type': 'group',
                'username': group.name,
                'name': group.name
                })
    print(f'list-of-contacts for {username}: {list_of_users + list_of_groups}')
    socketio.emit('get-list-of-contacts',
                list_of_users + list_of_groups,
                room=app.config['clients'][flask_login.current_user.username])

@socketio.on('disconnect')
def remove_client():
    print(f"Event for {flask_login.current_user.username}: disconnect")
    print(f"Username: {flask_login.current_user.username}")
    
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
                    'name': result.name}
    except Exception as e:
        print(e)
        data = {'answer': 'False'}
    print(data)
    socketio.emit('answerToDoesUsernameExists',
                data,
                room=app.config['clients'][flask_login.current_user.username])

if __name__ == '__main__':
    # app.run(debug=True)
    # socketio.run(app, port='80', host='0.0.0.0')
    socketio.run(app, debug=True)
