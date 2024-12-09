from app.models import book

def get_all_books():
    return book.query.all()