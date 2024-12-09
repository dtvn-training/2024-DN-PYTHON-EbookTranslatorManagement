from flask import Blueprint, jsonify
from app.controllers.book_control import get_all_books
books = Blueprint("books", __name__, url_prefix="/books")


@books.route("/")
def hello_world():
    return "Hello world!"


@books.route("/books")
def get_all_books():
    return jsonify(get_all_books())