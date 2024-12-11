from flask import Blueprint, jsonify
from app.controllers.book_control import get_all_books as get_all_books_control

books = Blueprint("books", __name__, url_prefix="/books")

@books.route("/")
def get_all_books():
    return jsonify(get_all_books_control())