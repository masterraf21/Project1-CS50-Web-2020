import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    JSON_SORT_KEYS = False
