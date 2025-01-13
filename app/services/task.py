from app.models import TaskCategory, Book, Profile, User, Chapter, Task, Language, Level
from app.interfaces import Task_Management, Task_Register, Response
from database.db import db
from sqlalchemy import func
import datetime, calendar
from collections import defaultdict


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
# code 1:success, 0: not found or registered, 2: over limit task
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

def count_total_task():
    total_task = Task.query.count()
    return total_task

def count_completed_task():
    completed_task = Task.query.filter(Task.is_completed == True).count()
    return completed_task

def count_uncompleted_task():
    uncompleted_task = Task.query.filter(Task.is_completed == False).count()
    return uncompleted_task

def get_days_in_month(month: int, year: int):
    if not isinstance(month, int) or not isinstance(year, int):
        raise ValueError("Month and Year must be integers")
    if year < 1:
        raise ValueError("Year must be a positive integer")

    if month > 12:
        month = 1
        year += 1

    if month < 1:
        month = 12
        year -= 1

    first_day, last_day = calendar.monthrange(year, month)
    start_of_month = datetime.date(year, month, 1)
    end_of_month = datetime.date(year, month, last_day)
    all_days = [start_of_month + datetime.timedelta(days=i) for i in range(last_day)]

    return start_of_month, end_of_month, all_days

def get_task_per_day(month: int, year: int):
    start_of_month, end_of_month, all_days = get_days_in_month(month, year)
    tasks_per_day = (
        Task.query
        .filter(Task.created_at >= start_of_month, Task.created_at <= end_of_month)
        .with_entities(
            func.date(Task.created_at).label('day'),
            Task.is_completed
        )
        .all()
    )
    task_count = defaultdict(lambda: {"completed": 0, "uncompleted": 0})

    for day, status in tasks_per_day:
        if status is True:
            task_count[day]["completed"] += 1
        else:
            task_count[day]["uncompleted"] += 1

    result = {str(day): task_count.get(day, {"completed": 0, "uncompleted": 0}) for day in all_days}

    return result

def get_task_per_month(month: int, year: int):

    start_of_month, end_of_month, all_days = get_days_in_month(month, year)

    tasks_per_day = (
        Task.query
        .filter(Task.created_at >= start_of_month, Task.created_at <= end_of_month, Task.is_completed == True)
        .with_entities(
            func.date(Task.created_at).label('day'),
            func.sum(Task.salary).label('total_salary')
        )
        .group_by(func.date(Task.created_at))
        .all()
    )

    task_data = {day: float(total_salary) for day, total_salary in tasks_per_day}

    result = {str(day): task_data.get(day, 0.0) for day in all_days}

    return result

def count_task_summary(month: int, year: int):
    task_per_day_data = get_task_per_day(month, year)
    total_completed = 0
    total_uncompleted = 0
    
    for day, counts in task_per_day_data.items():
        total_completed += counts.get("completed", 0)
        total_uncompleted += counts.get("uncompleted", 0)
    
    total_tasks = total_completed + total_uncompleted
    return {
        "total_tasks": total_tasks,
        "total_completed": total_completed,
        "total_uncompleted": total_uncompleted
    }

def get_tasks_to_table():
    all_tasks = Task.query.join(Chapter, Chapter.chapter_id == Task.chapter_id) \
                           .join(User, User.user_id == Task.user_id) \
                           .join(Book, Chapter.book_id == Book.book_id) \
                           .join(TaskCategory, TaskCategory.task_category_id == Task.task_category_id) \
                           .order_by((Task.created_at).desc()).limit(10).all()
    task_list = []
    for task in all_tasks:
        task_list.append({
            'task_id': task.task_id,
            'ebook': task.chapter.book.book_title,
            'chapter': task.chapter.chapter_title,
            'salary': task.salary,
            'owner': task.user.profile.fullname,
            'task_category': task.task_category.title,
            'completed': task.is_completed
        })
    
    return task_list