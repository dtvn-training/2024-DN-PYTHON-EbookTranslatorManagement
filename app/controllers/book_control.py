from app.services.book_services import get_all_books as get_books_from_service

def get_all_books():
    books = get_books_from_service()
    if not books:
        return None
    response = [book.to_dict() for book in books]
    return response