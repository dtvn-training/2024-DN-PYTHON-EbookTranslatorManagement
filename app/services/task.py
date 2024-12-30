from app.models import TaskCategory, Book, Profile, User, Chapter, Task
from app.interfaces import Task_Management
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
        Task.task_id, Chapter.chapter_title, Task.deadline, TaskCategory.title, Book.language,Profile.fullname)
    tasks = tasks.all()
    tasks = [Task_Management.create(task).to_dict() for task in tasks]
    return tasks

def count_total_task():
    return Task.query.count()

def count_task_current_month():
    current_month = datetime.now().month
    current_year = datetime.now().year
    return Task.query.filter(
        Task.deadline.isnot(None),
        Task.deadline.month == current_month,
        Task.deadline.year == current_year
    ).count() 

def count_completed_task():
    return Task.query.filter(Task.is_completed == True).count()

def count_uncompleted_task():
    return Task.query.filter(Task.is_completed == False).count()

def count_task_last_month():
    last_month = datetime.now().month - 1 if datetime.now().month != 1 else 12
    last_month_year = datetime.now().year if datetime.now().month != 1 else datetime.now().year - 1
    return Task.query.filter(
        Task.deadline.isnot(None),
        Task.deadline.month == last_month,
        Task.deadline.year == last_month_year
    ).count()


def count_task_each_day():
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    
    task_counts_per_day = {}
    tasks = Task.query.filter(Task.deadline >= start_of_month).all()

    for task in tasks:
        task_day = task.deadline.date()
        if task_day not in task_counts_per_day:
            task_counts_per_day[task_day] = 0
        task_counts_per_day[task_day] += 1

    return task_counts_per_day
