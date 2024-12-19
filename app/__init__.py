from flask import Flask
from database.db import db
from utils.secret import db_url
from app.views import books
from app.views import chapters
from app.views import tasks
from flask_cors import CORS

def register_blueprints(app):
    app.register_blueprint(books)
    app.register_blueprint(chapters)
    app.register_blueprint(tasks)

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    register_blueprints(app)
    with app.app_context():
        from .models import Level, Task, Chapter, User, TaskCategory, Book, Comment, Content, Notification, Profile, Role, KPI, UserNotification
        db.create_all()

    return app
