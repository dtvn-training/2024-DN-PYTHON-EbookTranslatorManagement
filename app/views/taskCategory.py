from flask import Blueprint, jsonify
from app.controllers.taskCategory import gets as get_task_controller, get_my_task_status_controller

taskCategory = Blueprint("taskCategory", __name__,
                         url_prefix="/api/task-category")


@taskCategory.route("/", methods=["GET"])
def gets():
    return jsonify(get_task_controller())


@taskCategory.route("/my-task", methods=["GET"])
def get_my_task_status():
    status = get_my_task_status_controller()
    if status["is_success"]:
        return jsonify(status), 200
    return jsonify(status), 400