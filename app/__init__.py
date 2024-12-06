from flask import Flask
from database.db import db
from .controllers.userController import user as userController
from utils.secret import db_url

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    app.register_blueprint(userController)
    with app.app_context():
        from .models.level import Level
        db.create_all()
    return app