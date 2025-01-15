from app.models import Task
from app.models import TaskCategory as TC
from database.db import db

def create_task(chapter_id, deadline, salary, task_category_id=1):
    try:
        new_task = Task(
            chapter_id=chapter_id,
            deadline=deadline,
            salary=salary,
            task_category_id=task_category_id
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task
    except Exception as e:
        db.session.rollback()
        return None
