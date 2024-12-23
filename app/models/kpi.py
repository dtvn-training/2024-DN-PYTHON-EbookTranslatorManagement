from database.db import db
from datetime import datetime
from decimal import Decimal


class KPI(db.Model):
    __tablename__ = 'kpi'

    kpi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey(
        "task.task_id"), nullable=False)
    salary = db.Column(db.Numeric(10, 2), default=Decimal('0.00'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Quan hệ với bảng User
    user = db.relationship('User', backref='kpis', lazy=True)
    task = db.relationship('Task', backref='kpis', lazy=True)

    def __init__(self, user_id, task_id, salary):
        self.user_id = user_id
        self.task_id = task_id
        self.salary = salary

    def to_dict(self):
        return {
            "kpi_id": self.kpi_id,
            "user_id": self.user_id,
            "salary": self.salary,
            "task_id": self.task_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
