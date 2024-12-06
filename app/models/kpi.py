from database.db import db
from datetime import datetime

class KPI(db.Model):
    __tablename__ = 'kpi'

    kpi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    task_completed = db.Column(db.Integer, nullable=False, default=0)
    average_score = db.Column(db.Numeric(5, 2), nullable=False, default=0.00)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Quan hệ với bảng User
    user = db.relationship('User', backref='kpis', lazy=True)

    def __init__(self, user_id, task_completed=0, average_score=0.00):
        self.user_id = user_id
        self.task_completed = task_completed
        self.average_score = average_score

    def to_dict(self):
        return {
            "kpi_id": self.kpi_id,
            "user_id": self.user_id,
            "task_completed": self.task_completed,
            "average_score": self.average_score,
            "last_updated": self.last_updated,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
