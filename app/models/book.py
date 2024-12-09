from database.db import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'book'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_title = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(25))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, book_title, language=None):
        self.book_title = book_title
        self.language = language

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "book_title": self.book_title,
            "language": self.language,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
