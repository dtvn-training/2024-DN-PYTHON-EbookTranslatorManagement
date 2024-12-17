from flask import Blueprint, jsonify
from app.controllers.content import upload_content_controller, get_content_controller
from flask_jwt_extended import jwt_required

contents = Blueprint("contents", __name__, url_prefix="/api/content")


@contents.route("/")
def get_content():
    content = get_content_controller()
    if content["is_success"]:
        return jsonify(content), 200
    return jsonify(content), 400


@contents.route("/upload", methods=["POST"])
@jwt_required()
def upload_content():
    upload_content = upload_content_controller()
    if upload_content["is_success"]:
        return jsonify(upload_content), 201
    return jsonify(upload_content), 400
