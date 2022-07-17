import socketio
from src import create_app, User, Messages, db
from flask import request
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
    list_of_users = [{'username':user.username, 'name':user.name} for user in User.query.all()]
    socketio.emit('get-list-of-users', list_of_users, room=app.config['clients'][flask_login.current_user.username])

@socketio.on('disconnect')
def remove_client():
    print(f"Event for {flask_login.current_user.username} disconnect")
    print(f"Username: {flask_login.current_user.username}")
    
    app.config['clients'].pop(flask_login.current_user.username)

@socketio.on('req-list-of-messages')
def get_existing_messages(receiver):
    print(f"Event for {flask_login.current_user.username}: req-list-of-messages of {receiver}")
    sender = flask_login.current_user.username

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
    list_of_messages = []
    
    for message in messages:
        if message.sender == sender:
            class_name = 'sent'
        else:
            class_name = 'received'
    
        list_of_messages.append({
            'message': message.message,
            'class_name': class_name
            })
    # print(list_of_messages)
    socketio.emit('get-list-of-messages', list_of_messages, room=app.config['clients'][sender])

@socketio.on('send-message')
def handle_message(data):
    print(f"Event for {flask_login.current_user.username}: send-message")
    receiver = data['receiver']
    message = data['message']

    # Save the message to the database
    new_message = Messages()
    new_message.sender = flask_login.current_user.username
    new_message.receiver = receiver
    new_message.message = message
    db.session.add(new_message)
    db.session.commit()
    
    data_to_send = {
        'message'   :   message,
        'from'    :   flask_login.current_user.username
    }
    print(f"Data: {data_to_send}")

    socketio.emit('display-message', data_to_send, room=app.config['clients'][receiver])


if __name__ == '__main__':
    # app.run(debug=True)
    # socketio.run(app, port='80', host='0.0.0.0')
    socketio.run(app, debug=True)
