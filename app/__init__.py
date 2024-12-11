from flask import Flask
from database.db import db
from utils.secret import db_url, SECRET_KEY_JWT
from app.views import taskCategory, task, language, chapters, downloads, users
from flask_cors import CORS
from flask_jwt_extended import JWTManager

def register_blueprints(app):
    app.register_blueprint(books)
    app.register_blueprint(chapters)
    app.register_blueprint(tasks)

def create_app():
    app = Flask(__name__, static_url_path="/static")
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config["JWT_SECRET_KEY"] = SECRET_KEY_JWT
    jwt = JWTManager(app)
    db.init_app(app)
    register_blueprints(app)
    with app.app_context():
        from .models import Level, Task, Chapter, User, TaskCategory, Book, Comment, Content, Notification, Profile, Role, KPI, UserNotification
        db.create_all()

    return app
