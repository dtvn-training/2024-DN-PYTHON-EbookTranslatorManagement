from database.db import db
from datetime import datetime


class Chapter(db.Model):
    __tablename__ = 'chapter'

    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.book_id', ondelete='CASCADE'), nullable=False)
    chapter_title = db.Column(db.String(100), nullable=False)
    chapter_content = db.Column(db.Text)
    chapter_status = db.Column(
        db.String(50), default='Pending', nullable=False)
    filename = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relationship với bảng Book
    book = db.relationship('Book', backref='chapters', lazy=True)

    def __init__(self, book_id, chapter_title, filename, chapter_content=None, chapter_status='Pending'):
        self.book_id = book_id
        self.chapter_title = chapter_title
        self.chapter_content = chapter_content
        self.chapter_status = chapter_status
        self.filename = filename

    def to_dict(self):
        return {
            "chapter_id": self.chapter_id,
            "book_id": self.book_id,
            "chapter_title": self.chapter_title,
            "chapter_content": self.chapter_content,
            "chapter_status": self.chapter_status,
            "filename": self.filename,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
