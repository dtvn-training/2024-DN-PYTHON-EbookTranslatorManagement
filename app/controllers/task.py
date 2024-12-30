from dateutil import parser
from app.services.task import get_tasks
from flask import request


def get_tasks_controllers(key="", deadline=None, task_category_id=None):
    key = request.args.get("key", "")
    deadline = request.args.get("deadline", None)
    task_category_id = request.args.get("task_category_id", None)
    if deadline:
        deadline = parser.parse(deadline)
        deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
    tasks = get_tasks(key, deadline, task_category_id)
    return tasks


