from app.services.comment import get_comments_service
from app.interfaces import Response


def get_comments_controller(task_id):
    try:
        if not task_id or not str(task_id).isdigit():
            return Response.create(False, "Invalid task_id. It must be a valid integer.", None)
        task_id = int(task_id)
        comments, code = get_comments_service(task_id)
        if comments:
            return Response.create(True, "Success to get comments", comments)
        if code == 2:
            return Response.create(True, "Comments not found", None)
        return Response.create(False, "Fail to get comments", None)
    except:
        return Response.create(False, "Fail to get comments", None)
