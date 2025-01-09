from flask import Blueprint, jsonify
from app.controllers.language import gets_controller

language = Blueprint('language', __name__, url_prefix="/api/language")


@language.route("/", methods=["GET"])
def gets():
    return jsonify(gets_controller())
