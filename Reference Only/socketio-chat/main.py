"""
TASK
----

Build a sample chatting app.
-> Enter a name
-> Enter a chat room
"""

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
from numpy import broadcast

app = Flask(__name__)
app.config['SECRET KEY'] = 'ThisTheIsKeySecret'     # For SocketIo
app.secret_key = 'ThisTheIsKeySecret'               # For Session
socketio = SocketIO(app)


# App Routes
@app.route('/', methods=["POST", "GET"])
def login_page():
    return render_template('login.html')

@app.route('/chat', methods=["POST", "GET"])
def chat_page():
    if request.method == 'POST':
        global username
        username = request.form.get('username')
        session['username'] = username
        session['logged_in'] = True
        return render_template('chat.html')
    else:
        if 'logged_in' in session.keys():
            return render_template('chat.html')


# Socket Events
@socketio.on('my event')
def handle_my_event(data):
    print(data['data'])


@socketio.on('send message')
def handle_send_message(message):
    msg = message['message']
    print(msg)
    msg = f"{session['username']}:  {msg}"
    socketio.emit('server broadcast', msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
