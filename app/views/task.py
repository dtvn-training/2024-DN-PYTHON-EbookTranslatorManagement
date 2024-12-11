from app.controllers.task import get_tasks_controllers
from flask import jsonify, Blueprint, request

task = Blueprint('task', __name__, url_prefix="/api/task")


@task.route("/")
def get_tasks():
    return jsonify(get_tasks_controllers())
