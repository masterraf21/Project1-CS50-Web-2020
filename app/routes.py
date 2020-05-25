from app import app
from flask_login import current_user, login_user, logout_user, login_required
from flask import Flask, session, render_template, request, abort, jsonify, g, url_for, redirect, flash, request, g
from app.models import *
from app.forms import *
from app.goodreads import Goodreads
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
    return render_template('register.html', form=form, title='Register')


@app.route('/search/<int:isbn>', methods=['GET'])
@login_required
def books(isbn):
    pass


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def books(book_id):
    # Get book by id, set in the session variable
    session['book'] = Book.getBook_id(book_id)
    # Check if book is not available
    if session['book'] == None:
        abort(404)
    else:
        # if available create a new book object from JSON
        book_json = json.loads(session['book'])
        book = Book.getBookfromJSON(book_json)
        
    # Get user's review
    ureview = Review.getReview_uid_bookid(current_user.id,book_id)
    # Get book's review and count
    breview = Review.getReview_bookid(book_id)
    if breview != None:
        breview_count = 0
    else:
        breview_count =len(breview)
    # Count book's rating
    if breview_count == 0:
        breview_avgrating = 0
    else:
        breview_avgrating = Review.getAvgRating(breview)
    
    # Get goodreads object
    greadsObject = Goodreads(book.isbn)
    greadsObject.getGoodreadsData()
  
    # Set form review
    form = ReviewForm()
    # Check if POST is successful
    if form.validate_on_submit:
        # Check if user already review the book
        if ureview == None:
            # Create review from POST
            Review.create(form.rating.data,form.review.data,current_user.id,book.id)
            # Set session var review
            session['reviewStatus'] = 1
            # return redirect(url_for('revsubmit'))
        else:
            session['reviewStatus'] = 0
            # return redirect(url_for('revsubmit'))

    return render_template('book.html', book=book, form=form, greads=greadsObject, avgRating=breview_avgrating, ratingCount=breview_count)

