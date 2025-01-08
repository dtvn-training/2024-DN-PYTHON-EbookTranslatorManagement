from app.models import TaskCategory, Book, Profile, User, Chapter, Task
from app.interfaces import Task_Management
from sqlalchemy import func
import datetime
from collections import defaultdict

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
        Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Book.language_id, Profile.fullname)
    tasks = tasks.all()
    tasks = [Task_Management.create(task).to_dict() for task in tasks]
    return tasks

def get_total_task():
    total_task = Task.query.count()
    return total_task

def get_completed_task():
    completed_task = Task.query.filter(Task.is_completed == True).count()
    return completed_task

def get_uncompleted_task():
    uncompleted_task = Task.query.filter(Task.is_completed == False).count()
    return uncompleted_task

def count_task_per_day(month: int, year: int):
    if month < 1:
        month = 12
        year -= 1
    
    start_of_month = datetime.datetime(year, month, 1)
    if month == 12:
        end_of_month = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(seconds=1)
    else:
        end_of_month = datetime.datetime(year, month + 1, 1) - datetime.timedelta(seconds=1)
    
    all_days = [
        (start_of_month + datetime.timedelta(days=i)).date()
        for i in range((end_of_month - start_of_month).days + 1)
    ]
    
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
    if month < 1:
        month = 12
        year -= 1
    
    start_of_month = datetime.datetime(year, month, 1)
    if month == 12:
        end_of_month = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(seconds=1)
    else:
        end_of_month = datetime.datetime(year, month + 1, 1) - datetime.timedelta(seconds=1)
    
    all_days = [
        (start_of_month + datetime.timedelta(days=i)).date()
        for i in range((end_of_month - start_of_month).days + 1)
    ]

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
    task_per_day_data = count_task_per_day(month, year)
    
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



