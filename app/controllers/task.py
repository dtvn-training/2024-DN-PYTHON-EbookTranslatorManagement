from dateutil import parser
from flask import request
import datetime
from flask_jwt_extended import get_jwt_identity
from app.interfaces import Response
from app.services.task import (
    get_tasks,
    get_total_task,
    get_completed_task,
    get_uncompleted_task,
    get_task_per_month,
    count_task_per_day,
    count_task_summary,
    get_tasks_to_table,
    get_register_tasks_service,
    register_task_service
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

def get_task_summary_controllers():
    now = datetime.datetime.now()
    current_month = now.month
    current_year = now.year

    total_task = get_total_task()
    completed_task = get_completed_task()
    uncompleted_task = get_uncompleted_task()

    tasks_per_day = count_task_per_day(current_month, current_year)
    tasks_per_day_current_month = get_task_per_month(current_month, current_year)
    tasks_per_day_last_month = get_task_per_month(current_month - 1, current_year)
    count_task_in_month = count_task_summary(current_month, current_year)

    return {
        "total_task": total_task,
        "completed_task": completed_task,
        "uncompleted_task": uncompleted_task,
        "count_task_of_month": count_task_in_month,
        "count_task_per_day": tasks_per_day,
        "tasks_per_day_current_month": tasks_per_day_current_month,
        "tasks_per_day_last_month": tasks_per_day_last_month
    }

def get_tasks_to_table_controllers():
    tasks = get_tasks_to_table()
    return tasks

def get_register_tasks_controller():
    key = request.args.get("key", "")
    type = request.args.get("type", "")
    language = request.args.get("language", "")
    tasks = get_register_tasks_service(key, type, language)
    return tasks


def registe_task_controller(task_id):
    try:
        id = int(task_id)
        user = get_jwt_identity()
        register = register_task_service(id, user["user_id"])
        if register == 0:
            return Response.create(False, "Task not found or registered", None)
        if (register == 2):
            return Response.create(False, "The number of tasks is enough for your level", None)
        return Response.create(True, "Task registered successfully", None)
    except Exception as e:
        return Response.create(False, "Fail for registration", None)
