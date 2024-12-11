from app.models import Book

def get_all_books():
    books = Book.query.all()
    return books
