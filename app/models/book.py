from database.db import db
from datetime import datetime


class Book(db.Model):
    __tablename__ = 'book'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_title = db.Column(db.String(100), nullable=False)
    language_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, book_title, language_id=None):
        self.book_title = book_title
        self.language_id = language_id

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "book_title": self.book_title,
            "language_id": self.language_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
