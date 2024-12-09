from app.services.book_services import get_all_books

def get_all_books():
    books = get_all_books()
    if not books:
        return None
    response = [book.to_dict() for book in books]
    return response
