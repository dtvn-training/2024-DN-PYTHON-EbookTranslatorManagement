from app.models import Book
from database.db import db


def upload_book_service(book_title, language_id):
    book = Book(book_title,language_id)
    db.session.add(book)
    return True
