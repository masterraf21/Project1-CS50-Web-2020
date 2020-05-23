from app import app
from flask_login import current_user, login_user, logout_user, login_required
from flask import Flask, session, render_template, request, abort, jsonify, g, url_for, redirect, flash, request
from app.models import User
from app.forms import LoginForm, RegistrationForm
from werkzeug.urls import url_parse

# Add decorator : @login_required for protecting some routes from anonymous user

# TODO add Search 
# TODO add Review
# TODO create book page
# TODO get review from Goodreads
# TODO API for books by isbn


@app.route('/')
@app.route('/index')
def index():
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is authenticated already
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Create form for login use
    form = LoginForm()
    # Check submit by POST
    if form.validate_on_submit():
        user = User.getUser_username(username=form.username.data)
        if user and user.check_password(password=form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password! Please Sign Up!')
    # Render for GET only
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user is authenticated already
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # Create form for register 
    form = RegistrationForm()
    # Check submitted by POST
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.createUser()
        flash('Congratulations! Your account has been Created')
        return redirect(url_for('login'))
    # Render for GET only
    return render_template('register.html', form=form, title = 'Register')


    