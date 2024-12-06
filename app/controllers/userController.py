from flask import Blueprint
from app.models.level import Level
from database.db import db

user = Blueprint('user', __name__)


@user.route("/")
def index():
    data = db.session.query(Level).all()
    for level in data:
        print(level.to_dict())
    return "data"
