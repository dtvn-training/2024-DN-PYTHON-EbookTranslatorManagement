from flask import Flask
from database.db import db
from utils.secret import db_url, SECRET_KEY_JWT
from app.views import taskCategory, task, language, chapters, downloads, users, contents, comments
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__, static_url_path="/static")
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config["JWT_SECRET_KEY"] = SECRET_KEY_JWT
    app.config["JWT_VERIFY_SUB"] = False
    jwt = JWTManager(app)
    db.init_app(app)
    app.register_blueprint(taskCategory)
    app.register_blueprint(task)
    app.register_blueprint(language)
    app.register_blueprint(chapters)
    app.register_blueprint(downloads)
    app.register_blueprint(users)
    app.register_blueprint(contents)
    app.register_blueprint(comments)
    with app.app_context():
        from .models import Level, Task, Chapter, User, TaskCategory, Book, Comment, Content, Notification, Profile, Role, KPI, UserNotification
        db.create_all()
    return app
