from flask import Blueprint, jsonify
from app.controllers.taskCategory import gets as get_task_controller

taskCategory = Blueprint("taskCategory", __name__,
                         url_prefix="/api/task-category")


@taskCategory.route("/")
def gets():
    return jsonify(get_task_controller())
