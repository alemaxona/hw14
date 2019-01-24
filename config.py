__author__ = 'alemaxona'


from os import urandom


key = urandom(15)
# path_db = r'sqlite:///C:/sqlite/user_databases/hw14.db'  # win
path_db = 'postgresql://test:test@localhost/test_db'  # Connect to postgresql (pip install psycopg2)


class Configuration():
    DEBUG = True
    SECRET_KEY = key
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/alemaxona/Documents/Projects/hw14/app/db/hw14.db'  # mac
    SQLALCHEMY_DATABASE_URI = path_db
