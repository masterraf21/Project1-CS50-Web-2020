from app import db, login_manager, bcrypt
from flask_login import UserMixin
import json


@login_manager.user_loader
def load_user(id):
    return User.getUser_id(id)


class User(UserMixin):
    def __init__(self, username, id=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    def createUser(self):
        db.session.execute("INSERT INTO users (id, username, password) VALUES (:id, :username, :password)", {
                           "id": self.id, "username": self.username, "password": self.password})
        db.session.commit()

    def searchUser(self):
        pass

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    @classmethod
    def getUser_id(cls, id):
        response = db.session.execute(
            "SELECT * FROM users WHERE id = :id", {"id": id}).fetchone()
        # response = (id,username,password)
        # return newly created object
        return cls(response[1], response[0], response[2])

    @classmethod
    def getUser_username(cls, username):
        response = db.session.execute(
            "SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if response != None:
            return cls(response[1], response[0], response[2])
        else:
            return None


class Book():
    def __init__(self, id, isbn, author, title, year):
        self.id = id
        self.isbn = isbn
        self.author = author
        self.title = title
        self.year = year
    # Static methods for searching book based on their attributes
    # These methods will return json

    @staticmethod
    def getBook_id(id):
        # this method will return only one entry
        response = db.session.execute(
            "SELECT * from books WHERE id = :id", {"id": id}).fetchone()
        if response != None:
            return json.dumps(tuple(response))
        else:
            return None

    @staticmethod
    def getBook_isbn(isbn):
        # this method will return only one entry
        response = db.session.execute(
            "SELECT * from books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
        if response != None:
            return json.dumps(tuple(response))
        else:
            return None

    @staticmethod
    def getBook_author(author):
        # this method can return multiple entries
        books = list()
        response = db.session.execute(
            "SELECT * from books where author = :author", {"author": "%"+author+"%"}).fetchmany(40)
        if response != None:
            for res in response:
                books.append(json.dumps(tuple(res)))
            return books
        else:
            return None

    @staticmethod
    def getBook_title(title):
        # this method can return multiple entries
        books = list()
        response = db.session.execute(
            "SELECT * FROM books WHERE title = :title", {"title": "%"+title+"%"}).fetchmany(40)
        if response != None:
            for res in response:
                books.append(json.dumps(tuple(res)))
            return books
        else:
            return None

    @staticmethod
    def getBook_year(year):
        # this method can return multiple entries
        books = list()
        response = db.session.execute(
            "SELECT * FROM books WHERE year = :year", {"year": "%"+year+"%"})
        if response != None:
            for res in response:
                books.append(json.dumps(tuple(res)))
            return books
        else:
            return None

    @classmethod
    def getBookfromJSON(cls, book_json):
        b = json.loads(book_json)
        return cls(b[0], b[1], b[2], b[3], b[4])


class Review():
    def __init__(self, id, rating, review, user_id, book_id):
        self.id = id
        self.rating = rating
        self.review = review
        self.user_id = user_id
        self.book_id = book_id

    @staticmethod
    def create(rating, review, user_id, book_id):
        db.session.execute(
            "INSERT INTO reviews(rating,review,user_id,book_id) VALUES (:rating, :review, :user_id, :book_id)", {"rating": rating, "review": review, "user_id": user_id, "book_id": book_id})
        db.session.commit()

    @staticmethod
    def getReview_uid_bookid(user_id, book_id):
        # A user can only review once on a book
        response = db.session.execute(
            "SELECT * FROM reviews where user_id = :user_id AND book_id = :book_id", {"user_id": user_id, "book_id": book_id}).fetchone()
        if response != None:
            return json.dumps(response)
        else:
            return None

    @staticmethod
    def getReview_uid(user_id):
        # A user can have many reviews
        reviews = list()
        response = db.session.execute(
            "SELECT * FROM reviews WHERE user_id = :user_id", {"user_id": user_id}).fetchmany(40)
        if response != None:
            for res in response:
                reviews.append(json.dumps(tuple(res)))
            return reviews
        else:
            return None

    @staticmethod
    def getReview_bookid(book_id):
        # A book can have many reviews
        reviews = list()
        response = db.session.execute(
            "SELECT * FROM reviews WHERE book_id = :book_", {"book_id": book_id}).fetchmany(40)
        if response != None:
            for res in response:
                reviews.append(json.dumps(tuple(res)))
            return reviews
        else:
            return None

    @staticmethod
    def getAvgRating(list_of_reviews: list):
        # Get average rating from list of JSON Reviews
        count = len(list_of_reviews)
        total_rating = 0
        for review in list_of_reviews:
            review = json.loads(review)
            total_rating += review[1] #review.rating
        avg_rating = float(total_rating) / float(count)

        return avg_rating

    @classmethod
    def getReviewFromJSON(cls, review_json):
        r = json.loads(review_json)
        return cls(r[0], r[1], r[2], r[3])
