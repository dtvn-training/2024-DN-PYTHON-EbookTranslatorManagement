from flask import Blueprint, jsonify
from app.controllers.book import progress_tracking_controller

books = Blueprint("books", __name__, url_prefix="/api/ebook")


@books.route("/proress-tracking", methods=["GET"])
def progress_tracking():
    # progress_tracking_controller()
    return jsonify(progress_tracking_controller())
