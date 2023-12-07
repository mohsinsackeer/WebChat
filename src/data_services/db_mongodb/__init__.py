from src.data_services.db_mongodb.mongodb_utils import MongoAppDB
from flask_login import LoginManager

# from src.auth import auth
# from src.chat import chat

db = MongoAppDB()

"""
def app_and_mongodb(app):
    db = MongoAppDB()
    
    with app.app_context():
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login_page'
        login_manager.init_app(app)
        
        @login_manager.user_loader
        def load_user(user_id):
            return db.get_user(user_id)

        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(chat, url_prefix='/')
    
    return app, db
"""

__all__ = [
    "db"
]