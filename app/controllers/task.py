from dateutil import parser
from app.services.task import get_tasks, get_register_tasks_service, get_task_content_service, register_task_service, get_information_task_service
from flask import request
from flask_jwt_extended import get_jwt_identity
from app.interfaces import Response


def get_tasks_controllers(key="", deadline=None, task_category_id=None):
    key = request.args.get("key", "")
    deadline = request.args.get("deadline", None)
    task_category_id = request.args.get("task_category_id", None)
    if deadline:
        deadline = parser.parse(deadline)
        deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
    tasks = get_tasks(key, deadline, task_category_id)
    return tasks


def get_content_controllers(task_id):
    if not task_id or not str(task_id).isdigit():
        return Response.create(False, "Invalid task_id. It must be a valid integer.", None)
    task_content = get_task_content_service(task_id)
    if task_content:
        return Response.create(True, "Success to get task content", task_content)
    return Response.create(False, "Task content not found", None)


def get_register_tasks_controller():
    key = request.args.get("key", "")
    type = request.args.get("type", "")
    language = request.args.get("language", "")
    tasks = get_register_tasks_service(key, type, language)
    return tasks


def registe_task_controller(task_id):
    try:
        id = int(task_id)
        user = get_jwt_identity()
        register = register_task_service(id, user["user_id"])
        if register == 0:
            return Response.create(False, "Task not found or registered", None)
        if (register == 2):
            return Response.create(False, "The number of tasks is enough for your level", None)
        return Response.create(True, "Task registered successfully", None)
    except Exception as e:
        return Response.create(False, "Fail for registration", None)


def get_information_task_controller(task_id):
    try:
        if not task_id or not str(task_id).isdigit():
            return Response.create(False, "Task id must be a number", None)
        task_id = int(task_id)
        task_information = get_information_task_service(task_id)
        if task_information:
            return Response.create(True, "Get task information successfully", task_information)
        return Response.create(False, "Task information not found", None)
    except:
        return Response.create(False, "Fail to get task information", None)
