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
        db.session.execute("INSERT INTO users (id, username, password) VALUES (:id, :username, :password)",{"id": self.id, "username": self.username, "password": self.password})
        db.session.commit()

    def searchUser(self):
        pass
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)


    @classmethod
    def getUser_id(cls, id):
        data = db.session.execute("SELECT * FROM users WHERE id = :id",{"id": id}).fetchone()
        #response = (id,username,password)
        #return newly created object
        return cls(data[1],data[0],data[2])


    @classmethod
    def getUser_username(cls, username):
        data = db.session.execute("SELECT * FROM users WHERE username = :username",{"username":username}).fetchone()
        if data != None:
            return cls(data[1],data[0],data[2])
        else:
            return None
    


        

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

