from app.controllers.task import get_tasks_controllers, get_register_tasks_controller, registe_task_controller
from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required

task = Blueprint('task', __name__, url_prefix="/api/task")


@task.route("/")
def get_tasks():
    return jsonify(get_tasks_controllers())


# routes for register task
@task.route("/registe-task", methods=["GET"])
def register_task():
    return jsonify(get_register_tasks_controller())


@task.route("/register-task/<task_id>", methods=["POST"])
@jwt_required()
def register_task_by_id(task_id):
    task = registe_task_controller(task_id)
    if task["success"]:
        return jsonify(task), 201
    return jsonify(task), 400
