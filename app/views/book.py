from flask import Blueprint, jsonify
from app.controllers.book import progress_tracking_controller

books = Blueprint("books", __name__, url_prefix="/api/ebook")


@books.route("/progress-tracking", methods=["GET"])
def progress_tracking():
    progress_tracking = progress_tracking_controller()
    if progress_tracking["is_success"]:
        return jsonify(progress_tracking), 200
    return jsonify(progress_tracking), 400
