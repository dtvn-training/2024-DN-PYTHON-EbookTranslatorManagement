from database.db import db
from datetime import datetime


class MyTask(db.Model):
    __tablename__ = 'my_task'

    my_task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey(
        'task.task_id', ondelete='CASCADE'), nullable=False)
    status_task_id = db.Column(db.Integer, db.ForeignKey(
        'status_task.status_task_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Quan hệ với bảng StatusTask
    status = db.relationship(
        'StatusTask', back_populates='task_entries', lazy=True)

    def __init__(self, user_id, task_id, status_task_id):
        self.user_id = user_id
        self.task_id = task_id
        self.status_task_id = status_task_id

    def to_dict(self):
        return {
            "my_task_id": self.my_task_id,
            "user_id": self.user_id,
            "task_id": self.task_id,
            "status_task_id": self.status_task_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
