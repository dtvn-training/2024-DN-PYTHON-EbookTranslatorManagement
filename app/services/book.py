from app.models import Book, Chapter, Task, Language, TaskCategory
from app.interfaces import Progress, Book as BookInterface


def progress_tracking_service(offset, limit, key, language_id):
    try:
        books, total_record = get_book(offset, limit, key, language_id)
        book_ids = [book["book_id"] for book in books]
        progress = Chapter.query.filter(Book.book_id.in_(book_ids)).join(Book, Book.book_id == Chapter.book_id).join(
            Task, Chapter.chapter_id == Task.chapter_id, isouter=True
        ).join(
            Language, Language.language_id == Book.language_id
        ).join(
            TaskCategory, TaskCategory.task_category_id == Task.task_category_id, isouter=True
        ).with_entities(Book.book_id, Book.book_title, Language.title, Chapter.chapter_id, Chapter.chapter_title, Task.task_id, Task.is_completed, TaskCategory.title).all()
        progress = [Progress.create(item) for item in progress]
        return progress, total_record
    except:
        return None, None


def get_book(offset, limit, key, language_id):
    progress = Book.query.filter(
        Book.book_title.like(f"%{key}%"),
    ).join(
        Language, Language.language_id == Book.language_id
    )
    if language_id:
        progress = progress.filter(Language.language_id == language_id)
    total_record = progress.count()
    progress = progress.offset(offset).limit(
        limit
    ).with_entities(Book.book_id, Book.book_title, Language.title).all()
    if not progress:
        return [], 0
    progress = [BookInterface.create(item) for item in progress]
    return progress, total_record
