from flask import Blueprint, jsonify
from app.controllers.book import upload_book_controller

books = Blueprint("books", __name__, url_prefix="/api/ebook")


@books.route("/upload", methods=["POST"])
def upload_ebook():
    response = upload_book_controller()
    if response["success"]:
        return jsonify(response), 201
    return jsonify(response), 400
