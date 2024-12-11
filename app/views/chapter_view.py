from flask import Blueprint, jsonify
from app.controllers.chapter_control import get_all_chapters as get_all_chapters_control, get_chapters_by_book_id as get_chapters_by_book_id_control

chapters = Blueprint("chapters", __name__, url_prefix="/api/chapters")

@chapters.route("/")
def get_all_chapters():
    return jsonify(get_all_chapters_control())

@chapters.route("/<book_id>", methods=["GET"])
def get_chapter_by_book_id(book_id):
    return jsonify(get_chapters_by_book_id_control(book_id))