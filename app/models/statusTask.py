from database.db import db


class StatusTask(db.Model):
    __tablename__ = 'status_task'

    status_task_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    status_title = db.Column(db.String(55), nullable=False)

    # Quan hệ với bảng MyTask
    task_entries = db.relationship('MyTask', back_populates='status', lazy=True)

    def __init__(self, status_title):
        self.status_title = status_title

    def to_dict(self):
        return {
            "status_task_id": self.status_task_id,
            "status_title": self.status_title,
        }
