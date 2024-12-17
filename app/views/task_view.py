from flask import Blueprint, request, jsonify
from app.controllers.task_control import create_task as create_task_control

tasks = Blueprint("tasks", __name__, url_prefix="/api/tasks")

@tasks.route("/", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input data."}), 400

    required_fields = ['chapter_id', 'deadline','salary']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    created_task, error = create_task_control(data)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify(created_task.to_dict()), 201

