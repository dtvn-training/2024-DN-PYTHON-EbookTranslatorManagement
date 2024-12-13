from app.models import Task
from database.db import db


def create_task(book_id, chapter_id, deadline, salary):
    try:
        new_task = Task(
            book_id=book_id,
            chapter_id=chapter_id,
            deadline=deadline,
            salary=salary
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task  # Trả về đối tượng Task
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while creating the task: {e}")
        return None



    