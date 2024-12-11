from database.db import db
from sqlalchemy import CheckConstraint


class Language(db.Model):
    __tablename__ = 'language'

    language_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, title):
        self.title = title

    def to_dict(self):
        return {
            "language_id": self.language_id,
            "title": self.title
        }
