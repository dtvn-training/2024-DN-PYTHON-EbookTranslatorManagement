from flask import Blueprint, request, jsonify
from app.controllers.task_control import create_task as create_task_control

tasks = Blueprint("tasks", __name__, url_prefix="/api/tasks")

@tasks.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    created_task, error = create_task_control(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(created_task), 201