from flask import Blueprint, render_template
from flask_login import login_required
from src import User, db

chat = Blueprint('chat', __name__)

@chat.route('/chats')
@login_required
def chats():
    return render_template('chat/chats.html',
                            the_title='WebChat | Chat In To The Future')