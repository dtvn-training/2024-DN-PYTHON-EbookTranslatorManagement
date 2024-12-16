from flask import Blueprint, jsonify, send_from_directory
from app.controllers.chapter import get_content_controller, upload_chapter_controller

chapters = Blueprint("chapters", __name__, url_prefix="/api/chapter")


@chapters.route("/content/<chapter_id>")
def get_content(chapter_id):
    content = get_content_controller(chapter_id)
    return jsonify(content)


@chapters.route("/upload", methods=["POST"])
def upload_chapter():
    chapter = upload_chapter_controller()
    if chapter["success"]:
        return jsonify(chapter), 201
    return jsonify(chapter), 400
