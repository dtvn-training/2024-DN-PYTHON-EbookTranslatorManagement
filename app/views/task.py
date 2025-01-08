from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.task import (
    get_register_tasks_controller,
    registe_task_controller,
    get_tasks_controllers,
    get_task_summary_controllers,
    get_tasks_to_table_controllers
)

task = Blueprint('task', __name__, url_prefix="/api/task")


@task.route("/")
def get_tasks():
    return jsonify(get_tasks_controllers())


# routes for register task
@task.route("/registe-task")
def register_task():
    return jsonify(get_register_tasks_controller())


@task.route("/register-task/<task_id>", methods=["POST"])
@jwt_required()
def register_task_by_id(task_id):
    task = registe_task_controller(task_id)
    if task["success"]:
        return jsonify(task), 201
    return jsonify(task), 400

#Overview Data
@task.route("/dashboard")
def get_data_to_dashboard():
    data_dict = get_task_summary_controllers()
    return jsonify(data_dict)

#Table Data
@task.route("/table_tasks")
def get_table_tasks():
    print(get_tasks_to_table_controllers)
    return get_tasks_to_table_controllers()