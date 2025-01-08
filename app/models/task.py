from database.db import db
from datetime import datetime
from decimal import Decimal
from decimal import Decimal


class Task(db.Model):
    __tablename__ = 'task'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey(
        'chapter.chapter_id', ondelete='CASCADE'), nullable=False)
    task_name = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    is_completed = db.Column(db.Boolean, default=False)
    task_category_id = db.Column(
        db.Integer, db.ForeignKey('task_category.task_category_id'))
    salary = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    chapter = db.relationship('Chapter', backref='tasks', lazy=True)
    user = db.relationship('User', backref='tasks', lazy=True)
    task_category = db.relationship('TaskCategory', backref='tasks', lazy=True)

    def __init__(self, chapter_id, task_name, deadline, user_id=None, task_category_id=None, is_completed=False, salary=0):
        self.chapter_id = chapter_id
        self.task_name = task_name
        self.deadline = deadline
        self.salary = salary
        self.task_category_id = task_category_id
        self.is_completed = is_completed
        self.salary = salary

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_id": self.chapter_id,
            "task_name": self.task_name,
            "deadline": self.deadline,
            "salary": self.salary,
            "task_category_id": self.task_category_id,
            "salary": self.salary,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }