from app.models.task import Task
from app.models.chapter import Chapter
from app.models.content import Content
from app.models.user import User
from app.models.profile import Profile
from app.models.book import Book
from app.models.taskCategory import TaskCategory


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

    if deadline is not None:
        tasks = tasks.filter(Task.deadline <= deadline)
    if task_category_id is not None:
        tasks = tasks.filter(Task.task_category_id == task_category_id)
    tasks = tasks.with_entities(
        Task.task_id, Task.task_name, Task.deadline, Profile.fullname, Book.book_title, TaskCategory.title)
    tasks = tasks.all()
    return tasks
