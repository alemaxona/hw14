__author__ = 'alemaxona'


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Configuration
from model import *


app = Flask(__name__, template_folder='templates')
app.config.from_object(Configuration)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Hello world!'


if __name__ == "__main__":
    db.create_all()
    app.run()
