from app.models import Chapter

def get_all_chapters():
    chapters = Chapter.query.all()
    return chapters

def get_chapters_by_book_id(book_id):
    chapters = Chapter.query.filter_by(book_id=book_id).all()
    return chapters
