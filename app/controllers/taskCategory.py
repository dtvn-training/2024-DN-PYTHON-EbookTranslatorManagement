from app.services.taskCategory import gets as get_task_category_service, get_my_task_status_service
from app.interfaces import Response


def gets():
    task_categories = get_task_category_service()
    if not task_categories:
        return None
    response = [category.to_dict() for category in task_categories]
    return response


def get_my_task_status_controller():
    task_categories = get_my_task_status_service()
    if not task_categories:
        return Response.create(False, "Task category not found", None)
    return Response.create(True, "Get task category successfully", task_categories)
