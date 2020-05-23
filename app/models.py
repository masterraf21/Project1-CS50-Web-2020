from app import db, login
from flask_login import UserMixin
import json


@login.user_loader
def load_user(user_id):
    return User.getUser_id(user_id)


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def createUser(self):
        db.session.execute("INSERT INTO users (id, username, password) VALUES (:id, :username, :password)",{"id": self.id, "username": self.username, "password": self.password})
        db.session.commit()
        
    def searchUser(self):
        pass

    @classmethod
    def getUser_id(cls, id):
        pass

    @classmethod
    def getUser_username(cls, id):
        pass

class Book():
    def __init__(self, id, isbn, author, title, year):
        self.id = id
        self.isbn = isbn
        self.author = author
        self.title = title
        self.year = year


class Review():
    def __init__(self, id, book_id, user_id, rating, review):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.review = review

