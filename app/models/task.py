from database.db import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey(
        'chapter.chapter_id', ondelete='CASCADE'), nullable=False)
    task_name = db.Column(db.String(100))
    deadline = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    is_completed = db.Column(db.Boolean, default=False)
    task_category_id = db.Column(
        db.Integer, db.ForeignKey('task_category.task_category_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relationship với bảng Chapter, User và TaskCategory
    chapter = db.relationship('Chapter', backref='tasks', lazy=True)
    user = db.relationship('User', backref='tasks', lazy=True)
    task_category = db.relationship('TaskCategory', backref='tasks', lazy=True)

    def __init__(self,chapter_id, deadline,):
        self.chapter_id = chapter_id
        self.deadline = deadline

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "chapter_id": self.chapter_id,
            "deadline": self.deadline,
            "task_category_id": self.task_category_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
