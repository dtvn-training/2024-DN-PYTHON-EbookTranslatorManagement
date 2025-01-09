from flask import Blueprint, jsonify, send_from_directory
from app.controllers.chapter import get_content_controller, edit_chapter_controller, delete_chapter_controller

chapters = Blueprint("chapters", __name__, url_prefix="/api/chapter")


@chapters.route("/content/<chapter_id>")
def get_content(chapter_id):
    content = get_content_controller(chapter_id)
    return jsonify(content)


@chapters.route("/edit/<chapter_id>", methods=["POST"])
def edit_chapter(chapter_id):
    chapter = edit_chapter_controller(chapter_id)
    if chapter['is_success']:
        return jsonify(chapter), 200
    return jsonify(chapter), 400


@chapters.route("/delete/<chapter_id>", methods=["POST"])
def delete_chapter(chapter_id):
    chapter = delete_chapter_controller(chapter_id)
    if chapter['is_success']:
        return jsonify(chapter), 200
    return jsonify(chapter), 400
