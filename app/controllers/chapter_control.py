from app.services.chapter_services import get_all_chapters as get_chapters_from_service, get_chapters_by_book_id as get_chapters_by_book_id_services

def get_all_chapters():
    chapters = get_chapters_from_service()
    if not chapters:
        return None
    response = [chapter.to_dict() for chapter in chapters]
    return response

def get_chapters_by_book_id(book_id):
    if not book_id:
        raise ValueError("Book ID must be provided.")
    else:
        chapters = get_chapters_by_book_id_services(book_id)
        response = [chapter.to_dict() for chapter in chapters]
    return response
