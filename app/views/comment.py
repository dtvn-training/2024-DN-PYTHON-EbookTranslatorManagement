from flask import Blueprint, jsonify
from app.controllers.comment import get_comments_controller, confirm_comment_controller
from flask_jwt_extended import jwt_required

comments = Blueprint("comments", __name__, url_prefix="/api/comment")


@comments.route("/<task_id>", methods=["GET"])
def get_comments(task_id):
    comments = get_comments_controller(task_id)
    if comments["is_success"]:
        return jsonify(comments), 200
    return jsonify(comments), 400


@comments.route("/confirm-comment", methods=["POST"])
@jwt_required()
def confirm_comment():
    comment = confirm_comment_controller()
    if comment["is_success"]:
        return jsonify(comment), 200
    return jsonify(comment), 400
