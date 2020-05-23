import os
import csv

from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def load_data(file_name):
    file = open(file_name, mode='r')
    reader = csv.reader(file)
    return reader


def main():
    # create table users
    db.execute(
        "CREATE TABLE users(id serial PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    # create table books
    db.execute("CREATE TABLE books(id serial PRIMARY KEY, isbn VARCHAR NOT NULL, author VARCHAR NOT NULL, title VARCHAR NOT NULL, year INTEGER NOT NULL)")
    # create table reviews
    db.execute("CREATE TABLE reviews(id serial PRIMARY KEY, rating DECIMAL DEFAULT '0', review VARCHAR NOT NULL, user_id INTEGER references users NOT NULL, book_id INTEGER references books NOT NULL)")

    # load data from csv
    data = load_data("books.csv")
    for isbn, title, author, year in data:
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})

    # commit
    db.commit()


if __name__ == "__main__":
    main()
