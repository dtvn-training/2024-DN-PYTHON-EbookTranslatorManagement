from flask import Blueprint, jsonify
from app.controllers.comment import get_comments_controller

comments = Blueprint("comments", __name__, url_prefix="/api/comment")


@comments.route("/<task_id>")
def get_comments(task_id):
    comments = get_comments_controller(task_id)
    if comments["is_success"]:
        return jsonify(comments), 200
    return jsonify(comments), 400
