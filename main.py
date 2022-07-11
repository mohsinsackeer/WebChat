import socketio
from src import create_app, User
from flask import request, session
from flask_socketio import SocketIO
import flask_login

app = create_app()
app.config['SECRET KEY'] = 'ThisTheIsKeySecret'
app.config['clients'] = {}
socketio = SocketIO(app)

@socketio.on('connect')
def add_client():
    print("Event: connect")
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
    print("Event: disconnect")
    print(f"Username: {flask_login.current_user.username}")
    #username = flask_login.current_user.username
    #clients.pop(username)
    #print(f"len(clients) = {len(clients)}")
    app.config['clients'].pop(flask_login.current_user.username)

@socketio.on('send-message')
def handle_message(data):
    print("Event: send-message")
    receiver = data['receiver']
    message = data['message']
    # DO SOMETHING
    # user = flask_login.current_user
    # print(user.__dict__)
    # print(session)
    #print(message)
    #clients[receiver].emit()
    data_to_send = {
        'message'   :   message,
        'from'    :   flask_login.current_user.username
    }
    print(f"Data: {data_to_send}")
    socketio.emit('display-message', data_to_send, room=app.config['clients'][receiver])


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)
