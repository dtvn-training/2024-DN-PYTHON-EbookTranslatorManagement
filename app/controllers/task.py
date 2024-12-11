from dateutil import parser
from app.services.task import get_tasks, get_register_tasks_service, register_task
from flask import request
from flask_jwt_extended import get_jwt_identity


def get_tasks_controllers(key="", deadline=None, task_category_id=None):
    key = request.args.get("key", "")
    deadline = request.args.get("deadline", None)
    task_category_id = request.args.get("task_category_id", None)
    key = request.args.get("key", "")
    deadline = request.args.get("deadline", None)
    task_category_id = request.args.get("task_category_id", None)
    if deadline:
        deadline = parser.parse(deadline)
        deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
    tasks = get_tasks(key, deadline, task_category_id)
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
        register = register_task(id, user.user_id)
        print(register)
    except:
        return None
