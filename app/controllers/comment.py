from app.services.comment import get_comments_service, confirm_comment_service
from app.interfaces import Response, Status
from flask_jwt_extended import get_jwt_identity
from flask import request


def get_comments_controller(task_id):
    try:
        if not task_id:
            return Response.create(False, "Missing task_id", None)
        if not str(task_id).isdigit():
            return Response.create(False, "Invalid task_id. It must be a valid integer.", None)
        task_id = int(task_id)
        comments, code = get_comments_service(task_id)
        if comments:
            return Response.create(True, "Success to get comments", comments)
        if code == Status.NOTFOUND:
            return Response.create(True, "Comments not found", None)
        return Response.create(False, "Fail to get comments", None)
    except:
        return Response.create(False, "Fail to get comments", None)


def confirm_comment_controller():
    try:
        user = get_jwt_identity()
        user_id = user["user_id"]
        res_json = request.get_json()
        comment_id = res_json.get("comment_id", "")
        if not comment_id:
            return Response.create(False, "Comment id is required")
        if not str(comment_id).isdigit():
            return Response.create(False, "Invalid comment_id. It must be a valid integer.", None)
        comment, code = confirm_comment_service(comment_id, user_id)
        if comment:
            return Response.create(True, "Comment confirmed successfully", comment)
        if code == Status.NOTFOUND:
            return Response.create(True, "Comment not found", None)
        return Response.create(False, "Fail to confirm comment", None)
    except:
        return Response.create(False, "Fail to confirm comment", None)
