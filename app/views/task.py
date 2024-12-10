from app.controllers.task import get_tasks_controllers
from flask import jsonify, Blueprint, request

task = Blueprint('task', __name__, url_prefix="/api/task")


@task.route("/")
def get_tasks():
    key = request.args.get("key", "")
    deadline = request.args.get("deadline", None)
    task_category_id = request.args.get("task_category_id", None)
    return jsonify(get_tasks_controllers(key, deadline, task_category_id))
