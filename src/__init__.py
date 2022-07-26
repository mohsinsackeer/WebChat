from datetime import datetime
from zoneinfo import ZoneInfo
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import cloudinary_creds

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(80), index=True)
    dp_url = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, entered_password):
        return check_password_hash(self.password_hash, entered_password)
    
    def get_json_data(self):
        return {
            "username" : self.username,
            "name"  : self.name,
            "email" : self.email
        }

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80))
    receiver = db.Column(db.String(80))
    message = db.Column(db.String(256))
    time = db.Column(db.DateTime(timezone=True), default=datetime.now(tz=ZoneInfo('Asia/Kolkata')))

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True)
    members = db.Column(db.String(1215))
    admins = db.Column(db.String(1215))
    dp_url = db.Column(db.String(256))

class GroupMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80))
    sender = db.Column(db.String(80))
    message = db.Column(db.String(256))
    time = db.Column(db.DateTime(timezone=True), default=datetime.now(tz=ZoneInfo('Asia/Kolkata')))

def create_app():
    curr_dir = os.getcwd()
    database_path = os.path.join(curr_dir, 'database/db.sqlite')
    print(f'Database Path: {database_path}')
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'NoOneWillWillEverFigureOut.Ever!'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
    login_manager = LoginManager()

    with app.app_context():
        db.init_app(app)
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login_page'
        login_manager.init_app(app)

        # Create the following statement to retain the value in database
        # db.drop_all()
        db.create_all()

        # Creating a sample group (since creating from frontend is not yet possible)
        # grp = Groups()
        # grp.name = 'Changadam Boys'
        # grp.members = 'mohsinsackeer,admin1,admin2'
        # grp.admins = 'mohsinsackeer'
        # db.session.add(grp)
        # db.session.commit()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        
        from src.auth import auth
        from src.chat import chat
        
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(chat, url_prefix='/')

    return app


__all__ = [
    "create_app",
    "db",
    "User",
    "Messages",
    "Groups",
    "GroupMessages",
    "cloudinary_creds"
]
