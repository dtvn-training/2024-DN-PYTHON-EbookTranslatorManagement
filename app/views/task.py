from app.controllers.task import (
    get_tasks_controllers,
    get_task_summary_controllers,
    get_tasks_to_table_controllers
)
from flask import jsonify, Blueprint, request

task = Blueprint('task', __name__, url_prefix="/api/task")


@task.route("/")
def get_tasks_view():
    return jsonify(get_tasks_controllers())

@task.route("/dashboard")
def get_data_to_dashboard():
    data_dict = get_task_summary_controllers()
    return jsonify(data_dict)

@task.route("/table_tasks")
def get_table_tasks():
    print(get_tasks_to_table_controllers)
    return get_tasks_to_table_controllers()