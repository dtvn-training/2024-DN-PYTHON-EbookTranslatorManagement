from flask import Flask
from database.db import db
from utils.secret import db_url
from app.views import taskCategory, task, books
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    app.register_blueprint(taskCategory)
    app.register_blueprint(task)
    app.register_blueprint(books)
    with app.app_context():
        from .models import Level, Task, Chapter, User, TaskCategory, Book, Comment, Content, Notification, Profile, Role, KPI, UserNotification
        db.create_all()
    return app
