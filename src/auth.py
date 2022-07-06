import flask
from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_login import login_user
from src import User, db

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
    # remember = True if request.form['remember'] else False

    if not username or not entered_password:
        error_msg = "Missing Data"
        return render_template('auth/login_page.html',
                               error_msg=error_msg)

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(entered_password):
        error_msg = 'Your username-password combination does not match. Try Again!'
        return render_template('auth/login_page.html',
                                error_msg=error_msg)
    
    session.pop('username', None)
    login_user(user)
    return 'Success'


@auth.route('/signup_submit', methods=['POST'])
def signup_submit():
    error_msg = None
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if not (name or username or email or password):
        error_msg = 'Please enter all details, and Try Again!'
        return render_template('auth/signup_page.html',
                                error_msg=error_msg)

    if User.query.filter_by(username=username).count() == 1:
        error_msg = 'Username is already taken! Please try another username.'
        return render_template('auth/signup_page.html',
                                error_msg=error_msg)
    
    if User.query.filter_by(email=email).count() == 1:
        error_msg = "Email already taken. Please try again!"
        return render_template('auth/signup_page.html',
                                error_msg=error_msg)
    
    u = User()
    u.name = name
    u.username = username
    u.email = email
    u.set_password(password)
    # session['username'] = username
    session.pop('username', None)
    db.session.add(u)
    db.session.commit()
    login_user(u)

    return 'Success!'