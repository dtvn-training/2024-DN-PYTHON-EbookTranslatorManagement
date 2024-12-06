from database.db import db
from datetime import datetime

class Content(db.Model):
    __tablename__ = 'content'

    content_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Quan hệ với bảng Task
    task = db.relationship('Task', backref='contents', lazy=True)

    def __init__(self, content, task_id, status):
        self.content = content
        self.task_id = task_id
        self.status = status

    def to_dict(self):
        return {
            "content_id": self.content_id,
            "content": self.content,
            "task_id": self.task_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
