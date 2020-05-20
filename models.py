from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from passlib.apps import custom_app_context as pwd_context

db = SQLAlchemy()


class Book(db.Model):
    pass


class User(db.Model):
    pass
