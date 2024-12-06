from database.db import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comment'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey(
        'task.task_id', ondelete='CASCADE'))
    status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Quan hệ với bảng User và Task
    user = db.relationship('User', backref='comments', lazy=True)
    task = db.relationship('Task', backref='comments', lazy=True)

    def __init__(self, content, user_id, task_id=None, status=False):
        self.content = content
        self.user_id = user_id
        self.task_id = task_id
        self.status = status

    def to_dict(self):
        return {
            "comment_id": self.comment_id,
            "content": self.content,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
