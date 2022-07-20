from datetime import datetime
from zoneinfo import ZoneInfo
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password_hash = db.Column(db.String(80), index=True)
    # image = db.Column(db.String(256))

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
        db.drop_all()

        db.create_all()

        u = User()
        u.name = 'admin1'
        u.username = 'admin1'
        u.email = 'admin1'
        u.set_password('admin1')
        db.session.add(u)
        db.session.commit()

        u = User()
        u.name = 'admin2'
        u.username = 'admin2'
        u.email = 'admin2'
        u.set_password('admin2')
        db.session.add(u)
        db.session.commit()

        u = User()
        u.name = 'admin3'
        u.username = 'admin3'
        u.email = 'admin3'
        u.set_password('admin3')
        db.session.add(u)
        db.session.commit()

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
    "Messages"
]
