from app.models import TaskCategory, Book, Profile, User, Chapter, Task
from app.interfaces import Task_Management
from database import db
import datetime
def get_tasks(key, deadline, task_category_id):
    tasks = Task.query.join(Chapter, Task.chapter_id == Chapter.chapter_id).join(
        User, Task.user_id == User.user_id
    ).join(
        Profile, Profile.profile_id == User.profile_id
    ).join(
        Book, Book.book_id == Chapter.book_id
    ).join(
        TaskCategory, TaskCategory.task_category_id == Task.task_category_id
    ).filter(
        Chapter.chapter_title.like(f"%{key}%"),
        Task.is_completed == False
    )
    if deadline:
        tasks = tasks.filter(Task.deadline <= deadline)
    if task_category_id:
        tasks = tasks.filter(Task.task_category_id == task_category_id)
    tasks = tasks.with_entities(
        Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Book.language, Profile.fullname)
    tasks = tasks.all()
    tasks = [Task_Management.create(task).to_dict() for task in tasks]
    return tasks


def count_total_task():
    return Task.query.count()

def count_completed_task():
    return Task.query.filter(Task.is_completed == True).count()

def count_uncompleted_task():
    return Task.query.filter(Task.is_completed == False).count()

def get_task_summary():
    total_task = Task.query.count()
    completed_task = Task.query.filter(Task.is_completed == True).count()
    uncompleted_task = Task.query.filter(Task.is_completed == False).count()

    return {
        "total_task": total_task,
        "completed_task": completed_task,
        "uncompleted_task": uncompleted_task
    }


