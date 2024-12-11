from app.models import Task
from database.db import db


def create_task(chapter_id, deadline, user_id=None, task_category_id=None, is_completed=False):
    try:
        new_task = Task(chapter_id=chapter_id, deadline=deadline, user_id=user_id, task_category_id=task_category_id, is_completed=is_completed)
        db.session.add(new_task)
        db.session.commit()
        print(f"Task created successfully!")
        return new_task
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while creating the task: {e}")
        return None

    