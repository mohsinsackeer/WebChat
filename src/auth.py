import json
from bson import json_util
from flask import Blueprint, render_template, redirect, url_for, session, request
import flask_login
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required
from cloudinary import uploader
from cloudinary.utils import cloudinary_url
# from src.data_services.db_mongodb import M
from src import db
from src.utils import ChatUser

auth = Blueprint('auth', __name__)

@auth.route('/')
def base_link():
    return redirect(url_for('auth.login_page'))


@auth.route('/login_page')
def login_page():
    return render_template('auth/login_page.html',
                           the_title='Login')

@auth.route('/signup_page')
def signup_page():
    return render_template('auth/signup_page.html',
                           the_title='Sign Up')

@auth.route('/login_submit', methods=['POST'])
def login_submit():
    error_msg = None
    username = request.form['username']
    entered_password = request.form['password']
    remember = True if request.form.get('remember', False) else False

    if not username or not entered_password:
        error_msg = "Missing Data"
        return render_template('auth/login_page.html',
                               error_msg=error_msg)

    # user = User.query.filter_by(username=username).first()
    # if user is None or not user.check_password(entered_password):
    #     error_msg = 'Your username-password combination does not match. Try Again!'
    #     return render_template('auth/login_page.html',
    #                             error_msg=error_msg)
    
    login_successful = db.validate_pwd(username, entered_password)
    print(login_successful)
    if not login_successful:
        error_msg = 'Your username-password combination does not match. Try Again!'
        return render_template('auth/login_page.html',
                                error_msg=error_msg)
    
    # user = json.loads(json_util.dumps(db.get_user(username)))
    user = db.get_user(username)
    
    # session.pop('username', None)
    login_user(ChatUser(user), remember=remember)
    # session['username'] = username
    db.remove_from_online_users(username)
    # db.add_to_online_users(username,request.sid)
    #return 'Success'
    print('Currently Here')
    return redirect(url_for('chat.chats'))


@auth.route('/signup_submit', methods=['POST'])
def signup_submit():
    error_msg = None
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    image = request.files['image']

    if not (name or username or email or password):
        error_msg = 'Please enter all details, and Try Again!'
        return render_template('auth/signup_page.html',
                                error_msg=error_msg)

    # if User.query.filter_by(username=username).count() == 1:
    if db.does_user_exist(username):
        error_msg = 'Username is already taken! Please try another username.'
        return render_template('auth/signup_page.html',
                                error_msg=error_msg)
    
    # if User.query.filter_by(email=email).count() == 1:
    if db.is_email_already_used(email):
        error_msg = "Email already taken. Please try again!"
        return render_template('auth/signup_page.html',
                                error_msg=error_msg)
    
    if image:
        upload_result = uploader.upload(image)
        dp_url, options = cloudinary_url(
            upload_result['public_id'],
            crop="fill",
        )
    else:
        dp_url = 'https://png.pngitem.com/pimgs/s/150-1503945_transparent-user-png-default-user-image-png-png.png'
    print(dp_url)
    # u = User()
    # u.name = name
    # u.username = username
    # u.email = email
    # u.set_password(password)
    # u.dp_url = dp_url
    # session.pop('username', None)
    # db.session.add(u)
    # db.session.commit()
    # login_user(u)
    # session['username'] = username
    db.create_new_user(username, name, email, password, dp_url)
    return redirect(url_for('chat.chats'))

@auth.route('/logout')
@login_required
def logout():
    db.remove_from_online_users(flask_login.current_user.username)
    logout_user()
    # session.pop('username', None)
    return redirect(url_for('auth.login_page'))