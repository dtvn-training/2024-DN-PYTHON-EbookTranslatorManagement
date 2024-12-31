from dateutil import parser
from flask import request
from app.services.task import (
    get_tasks,
    count_completed_task,
    count_total_task,
    count_uncompleted_task,
    get_task_summary
)


def get_tasks_controllers(key="", deadline=None, task_category_id=None):
    key = request.args.get("key", "")
    deadline = request.args.get("deadline", None)
    task_category_id = request.args.get("task_category_id", None)
    if deadline:
        deadline = parser.parse(deadline)
        deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
    tasks = get_tasks(key, deadline, task_category_id)
    return tasks

def count_completed_task_controllers():
    completed = count_completed_task()
    return completed

def count_total_task_controllers():
    total_task = count_total_task()
    return total_task

def count_uncompleted_task_controllers():
    uncompleted_task = count_uncompleted_task()
    return uncompleted_task


def get_dashboard_data():
    data = get_task_summary()
    return data
    
