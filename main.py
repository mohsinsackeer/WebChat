import socketio
from src import create_app
from flask import request, session
from flask_socketio import SocketIO
import flask_login

app = create_app()
app.config['SECRET KEY'] = 'ThisTheIsKeySecret'
app.config['clients'] = {}
socketio = SocketIO(app)

@socketio.on('connect')
def add_client():
    #client = {flask_login.current_user : request.namespace}
    #clients.append(client)
    #print(f"len(clients) = {len(clients)}")
    #print(f"request.sid = {request.sid}")
    app.config['clients'][flask_login.current_user.username] = request.sid
    print(f'{flask_login.current_user.username}: {request.sid}')
    data_to_send = {
        'sender'  :   flask_login.current_user.username,
        'receiver'  :   'mohsinsackeer' if flask_login.current_user.username=='admin' else 'admin'
    }
    print(f"{flask_login.current_user.username}: {data_to_send}")
    socketio.emit('set-username', data_to_send, room=app.config['clients'][flask_login.current_user.username])

@socketio.on('disconnect')
def remove_client():
    #username = flask_login.current_user.username
    #clients.pop(username)
    #print(f"len(clients) = {len(clients)}")
    app.config['clients'].pop(flask_login.current_user.username)

@socketio.on('send message')
def handle_message(data):
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
        'sender'    :   flask_login.current_user.username,
        'receiver'  :   receiver
    }
    socketio.emit('trial-message', data_to_send, room=app.config['clients'][receiver])


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app, debug=True)