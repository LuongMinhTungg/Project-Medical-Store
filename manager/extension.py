from flask import request
from flask_sqlalchemy import SQLAlchemy
from manager.config import app

db = SQLAlchemy(app)


def check_data():
    c = request.headers.get('Content-Type')
    if c == 'application/json':
        data = request.json
    else:
        data = request.form
    return data
