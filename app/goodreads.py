import requests, json
import os

KEY = os.getenv("GOODREADS_KEY")

def getGoodreads(isbn):
    r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": KEY, "isbns": isbn})
    if r.status_code == 200:
        temp = r.json()
        work_ratings_count = temp["books"][0]["work_ratings_count"]
        average_rating = temp["books"][0]["average_rating"]
        out = {"rating_count": work_ratings_count, "rating_average": average_rating}
        return out
    


