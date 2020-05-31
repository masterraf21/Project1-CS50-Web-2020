import requests
import json
import os

KEY = os.getenv("GOODREADS_KEY")


class Goodreads():
    def __init__(self, isbn, rating_count=None, average_rating=None, sucess=None):
        self.rating_count = rating_count
        self.average_rating = average_rating
        self.isbn = isbn
        self.sucess = sucess

    def getGoodreadsData(self):
        r = requests.get("https://www.goodreads.com/book/review_counts.json",
                         params={"key": KEY, "isbns": self.isbn})
        if r.status_code == 200:
            temp = r.json()
            work_ratings_count = temp["books"][0]["work_ratings_count"]
            average_rating = temp["books"][0]["average_rating"]
            self.rating_count = work_ratings_count
            self.average_rating = average_rating
            sucess = True
        else:
            self.rating_count = None
            self.average_rating = None
            self.sucess = False


