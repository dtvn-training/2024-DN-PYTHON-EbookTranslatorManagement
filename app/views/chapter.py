from flask import Blueprint, jsonify, send_from_directory
from app.controllers.chapter import get_content_controller

chapters = Blueprint("chapters", __name__, url_prefix="/api/chapter")


@chapters.route("/content/<chapter_id>", methods=["GET"])
def get_content(chapter_id):
    content = get_content_controller(chapter_id)
    return jsonify(content)
