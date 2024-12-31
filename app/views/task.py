from app.controllers.task import (
    get_tasks_controllers,
    count_completed_task_controllers,
    count_total_task_controllers,
    count_uncompleted_task_controllers,
    get_task_summary
)
from flask import jsonify, Blueprint, request

task = Blueprint('task', __name__, url_prefix="/api/task")


@task.route("/")
def get_tasks_view():
    return jsonify(get_tasks_controllers())

@task.route("/completed-task")
def count_completed_task_view():
    return jsonify(count_completed_task_controllers())

@task.route("/uncompleted-task")
def count_uncompleted_task_view():
    return jsonify(count_uncompleted_task_controllers())

@task.route("/total-task")
def count_total_task_view():
    return jsonify(count_total_task_controllers())

@task.route("/dashboard")
def get_data_to_dashboard():
    data_dict = get_task_summary()
    return jsonify(data_dict)
