from app.models import TaskCategory, Book, Profile, User, Chapter, Task, Language, Level
from app.interfaces import Task_Management, Task_Register, Response
from database.db import db


def get_tasks(key, deadline, task_category_id):
    tasks = Task.query.join(
        Chapter, Task.chapter_id == Chapter.chapter_id
    ).join(
        User, Task.user_id == User.user_id
    ).join(
        Profile, Profile.profile_id == User.profile_id, isouter=True
    ).join(
        Book, Book.book_id == Chapter.book_id
    ).join(
        Language, Language.language_id == Book.language_id
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
        Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Language.title, Profile.fullname)
    tasks = tasks.all()
    tasks = [Task_Management.create(task).to_dict() for task in tasks]
    return tasks


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


def register_task_service(task_id, user_id):
    code = 1
    task = Task.query.get(task_id)
    if not task or task.user_id:
        code = 0
        return code
    user_information = User.query.join(
        Profile, Profile.profile_id == User.profile_id).join(
            Level, Profile.level_id == Level.level_id
    ).filter(
        User.user_id == user_id
    ).with_entities(Profile.task_quantity, Level.level_limit, Profile.profile_id).first()
    current_task_quantity = user_information[0]
    limit_task = user_information[1]
    profile_id = user_information[2]
    # check the number of task is enough or not
    if current_task_quantity >= limit_task:
        code = 2
        return code
    task.user_id = user_id
    profile = Profile.query.get(profile_id)
    profile.task_quantity += 1
    db.session.commit()
    return code
