from app.models import TaskCategory, Book, Profile, User, Chapter, Task, Language
from app.interfaces import Task_Management, Task_Register
from database.db import db


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


# get tasks for register task
def get_register_tasks_service(key, type, language):
    tasks = Task.query.join(Chapter, Task.chapter_id == Chapter.chapter_id).join(
        Book, Book.book_id == Chapter.book_id
    ).join(
        TaskCategory, TaskCategory.task_category_id == Task.task_category_id
    ).join(Language, Book.language_id == Language.language_id).filter(
        Chapter.chapter_title.like(f"%{key}%"),
        Task.is_completed == False,
        Task.user_id == None
    )
    if type:
        tasks = tasks.filter(TaskCategory.task_category_id == type)
    if language:
        tasks = tasks.filter(Book.language_id == language)
    tasks = tasks.with_entities(
        Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Language.title, Chapter.chapter_id, Task.salary)
    tasks = tasks.all()
    tasks = [Task_Register.create(task).to_dict() for task in tasks]
    return tasks


# member register task
def register_task(task_id, user_id):
    task = Task.query.get(task_id)
    if not task:
        return None
    task.user_id = user_id
    db.session.commit()
    return True
