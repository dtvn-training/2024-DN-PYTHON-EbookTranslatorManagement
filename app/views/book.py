from flask import Blueprint, jsonify
from app.controllers.book import progress_tracking_controller, progress_tracking_detail_controller, edit_book_controller, get_chapter_ebook_controller, book_management_controller

books = Blueprint("books", __name__, url_prefix="/api/ebook")


@books.route("/progress-tracking", methods=["GET"])
def progress_tracking():
    progress_tracking = progress_tracking_controller()
    if progress_tracking["is_success"]:
        return jsonify(progress_tracking), 200
    return jsonify(progress_tracking), 400


@books.route("/progress-tracking-detail/<book_id>", methods=["GET"])
def progress_tracking_detail(book_id):
    detail = progress_tracking_detail_controller(book_id)
    if detail["is_success"]:
        return jsonify(detail), 200
    return jsonify(detail), 400


@books.route("/edit/<book_id>", methods=["POST"])
def edit_book(book_id):
    book = edit_book_controller(book_id)
    if book["is_success"]:
        return jsonify(book), 200
    return jsonify(book), 400


@books.route("/get-chapter-ebook/<book_id>", methods=["GET"])
def chapter_ebook(book_id):
    book = get_chapter_ebook_controller(book_id)
    if book["is_success"]:
        return jsonify(book), 200
    return jsonify(book), 400


@books.route("/book-management", methods=["GET"])
def book_management():
    books = book_management_controller()
    if books["is_success"]:
        return jsonify(books), 200
    return jsonify(books), 400
