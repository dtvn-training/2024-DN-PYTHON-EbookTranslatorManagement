from flask import Blueprint, request, jsonify
from app.controllers.task_control import create_task as create_task_control

tasks = Blueprint("tasks", __name__, url_prefix="/api/tasks/create")

@tasks.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input data."}), 400

    if not isinstance(data, list):
        return jsonify({"error": "Input data must be a list of tasks."}), 400

    try:
        results = create_task_control(data)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    return jsonify(results), 201



