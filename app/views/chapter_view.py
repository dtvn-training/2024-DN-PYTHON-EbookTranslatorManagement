from flask import Blueprint, jsonify
from app.controllers.chapter_control import get_all_chapters as get_all_chapters_control

chapters = Blueprint("chapters", __name__, url_prefix="/chapters")

@chapters.route("/")
def get_all_chapters():
    return jsonify(get_all_chapters_control())