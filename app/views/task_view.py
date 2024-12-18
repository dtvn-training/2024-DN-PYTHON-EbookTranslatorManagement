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

    results = []
    for task in data:
        chapter_id = task.get('chapter_id')
        deadline = task.get('deadline')
        salary = task.get('salary')

        if not chapter_id or not deadline or not salary:
            results.append({"error": f"Missing fields for chapter_id {chapter_id or 'unknown'}"})
            continue

        new_task, error = create_task_control(task)
        if error:
            results.append({"error": error, "chapter_id": chapter_id})
        else:
            results.append(new_task.to_dict())

    return jsonify(results), 201



