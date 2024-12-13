from app.models import Task
from app.models import TaskCategory as TC
from database.db import db

def add_task_to_all_categories(chapter_id, deadline, salary):
    try:
        categories = TC.query.all()
        tasks = []
        for category in categories:
            new_task = create_task(chapter_id, deadline, salary, category.id)
            if new_task:
                tasks.append(new_task)
        return tasks  # Trả về danh sách các Task đã được tạo
    except Exception as e:
        print(f"An error occurred while adding tasks to categories: {e}")
        return None

def create_task(chapter_id, deadline, salary, task_category_id):
    try:
        new_task = Task(
            chapter_id=chapter_id,
            deadline=deadline,
            salary=salary,
            task_category_id=task_category_id
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task  # Trả về đối tượng Task
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred while creating the task: {e}")
        return None

