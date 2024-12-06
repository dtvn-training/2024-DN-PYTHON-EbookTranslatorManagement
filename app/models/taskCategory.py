from database.db import db


class TaskCategory(db.Model):
    __tablename__ = 'task_category'

    task_category_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(15), nullable=False)

    def __init__(self, title):
        self.title = title

    def to_dict(self):
        return {
            "task_category_id": self.task_category_id,
            "title": self.title,
        }
