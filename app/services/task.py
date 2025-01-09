from app.models import TaskCategory, Book, Profile, User, Chapter, Task, Language, Level
from app.interfaces import Task_Management, Task_Register, Response, Task_Content, Status, MyTask, CountAndRecord
from database.db import db


def get_tasks(key, deadline, task_category_id, current_page, limit):
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
    tasks = tasks.paginate(
        page=current_page, per_page=limit, error_out=False)
    tasks = [Task_Management.create(task).to_dict() for task in tasks]
    return tasks


def get_task_content_service(task_id):
    try:
        task = Task.query.filter_by(task_id=task_id).join(
            Chapter, Chapter.chapter_id == Task.chapter_id
        )
        task = task.with_entities(Task.task_id, Chapter.chapter_content)
        task = task.first()
        if not task:
            return None
        return Task_Content.create(task)
    except:
        return None
# get tasks for register task


def get_register_tasks_service(key, type, language, current_page, limit):
    try:
        tasks = Task.query.join(Chapter, Task.chapter_id == Chapter.chapter_id).join(
            Book, Book.book_id == Chapter.book_id
        ).join(
            TaskCategory, TaskCategory.task_category_id == Task.task_category_id
        ).join(Language, Book.language_id == Language.language_id).filter(
            Book.book_title.like(f"%{key}%"),
            Task.is_completed == False,
            Task.user_id == None
        )
        if type:
            tasks = tasks.filter(TaskCategory.task_category_id == type)
        if language:
            tasks = tasks.filter(Book.language_id == language)
        count_tasks = tasks.count()
        tasks = tasks.with_entities(
            Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Language.title, Chapter.chapter_id, Task.salary, Book.book_title)
        tasks = tasks.paginate(
            page=current_page, per_page=limit, error_out=False)
        # tasks = tasks.all()
        tasks = [Task_Register.create(task).to_dict() for task in tasks]
        tasks = CountAndRecord.create(count_tasks, tasks)
        return tasks
    except:
        return None


# member register task
def register_task_service(task_id, user_id):
    try:
        task = Task.query.get(task_id)
        if not task or task.user_id:
            return Status.NOTFOUND
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
            return Status.DISALLOW
        task.user_id = user_id
        profile = Profile.query.get(profile_id)
        profile.task_quantity += 1
        db.session.commit()
        return Status.SUCCESS
    except:
        db.session.rollback()
        return Status.ERROR


def get_information_task_service(task_id):
    try:
        task = Task.query.filter_by(task_id=task_id).join(
            Chapter, Chapter.chapter_id == Task.chapter_id
        ).join(
            Book, Book.book_id == Chapter.book_id
        ).join(
            Language, Language.language_id == Book.language_id
        ).join(
            TaskCategory, TaskCategory.task_category_id == Task.task_category_id
        ).with_entities(
            Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Language.title, Chapter.chapter_content
        ).first()
        if not task:
            return None
        task = Task_Content.create(task)
        return task
    except:
        return None


def get_my_task_service(user_id):
    try:
        tasks = Task.query.filter_by(user_id=user_id).join(
            Chapter, Chapter.chapter_id == Task.chapter_id
        ).join(
            Book, Book.book_id == Chapter.book_id
        ).join(
            Language, Language.language_id == Book.language_id
        ).join(
            TaskCategory, TaskCategory.task_category_id == Task.task_category_id
        ).with_entities(
            Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Language.title, Task.salary
        ).all()
        tasks = [MyTask.create(task) for task in tasks]
        if tasks:
            return tasks, Status.SUCCESS
        return None, Status.NOTFOUND
    except:
        return None, Status.ERROR
