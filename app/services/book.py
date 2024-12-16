from app.models import Book
from database.db import db


def upload_book_service(book_title, language_id):
    try:
        book = Book(book_title, language_id)
        db.session.add(book)
        db.session.commit()
        return book.to_dict()
    except:
        db.session.rollback()
        return False
