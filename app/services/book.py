from app.models import Book, Chapter, Task, Language, TaskCategory, User, Profile, Content
from app.interfaces import Progress, Progress_Detail, Status, GetBook
from app.interfaces.Progress import Book as BookInterface
from database.db import db
from utils.retry_decorator import retry_function_decorator


@retry_function_decorator(retries=2, timeout=2)
def progress_tracking_service(offset, limit, key, language_id):
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


@retry_function_decorator()
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


@retry_function_decorator(retries=2, timeout=2)
def progress_tracking_detail_service(book_id):
    book = Book.query.filter(Book.book_id == book_id).join(
        Language, Language.language_id == Book.language_id).with_entities(
            Book.book_id,
            Book.book_title,
            Language.title
    ).first()
    book = BookInterface.create(book)
    progress = Chapter.query.filter(Book.book_id == book_id).join(Book, Book.book_id == Chapter.book_id).join(
        Task, Chapter.chapter_id == Task.chapter_id, isouter=True
    ).join(
        Language, Language.language_id == Book.language_id
    ).join(
        TaskCategory, TaskCategory.task_category_id == Task.task_category_id, isouter=True
    ).join(
        User, User.user_id == Task.user_id, isouter=True
    ).join(
        Profile, Profile.profile_id == User.profile_id, isouter=True
    ).join(
        Content, Content.task_id == Task.task_id, isouter=True
    ).with_entities(Chapter.chapter_id, Chapter.chapter_title, Profile.fullname, Task.deadline, Task.is_completed, TaskCategory.title, Content.filename, Content.created_at, Chapter.chapter_position).all()
    progress = [Progress_Detail.create(item) for item in progress]
    return book, progress


@retry_function_decorator(retries=2, timeout=2)
def edit_book_service(book_id, book_title, language_id):
    book = Book.query.filter(Book.book_id == book_id).first()
    if not book:
        return None, Status.NOTFOUND
    if book_title:
        book.book_title = book_title
    if language_id:
        is_lanuage_id = Language.query.filter(
            Language.language_id == language_id).first()
        if is_lanuage_id:
            book.language_id = language_id
        else:
            return None, Status.DISALLOW
    db.session.commit()
    return book.to_dict(), Status.SUCCESS


@retry_function_decorator(retries=2, timeout=2)
def get_chapter_ebook_service(book_id):
    books = Book.query.filter(Book.book_id == book_id).join(
        Language, Language.language_id == Book.language_id
    ).join(
        Chapter, Chapter.book_id == Book.book_id, isouter=True
    ).with_entities(Book.book_id, Language.language_id, Book.book_title, Chapter.chapter_id, Chapter.chapter_title, Chapter.filename).all()
    books = [GetBook.create(book) for book in books]
    if not books:
        return None, Status.NOTFOUND
    response = group_chapter(books)
    return response, Status.SUCCESS


@retry_function_decorator(retries=2, timeout=2)
def book_management_service(offset, limit):
    books = Book.query.join(
        Language, Language.language_id == Book.language_id
    ).offset(offset).limit(limit).with_entities(Book.book_id, Book.book_title, Language.title).all()
    books = [BookInterface.create(book) for book in books]
    total_record = Book.query.count()
    return {
        "book": books,
        "total_record": total_record,
    }, Status.SUCCESS


def group_chapter(books):
    chapters = []
    for book in books:
        if book["chapter_id"]:
            chapters.append({
                "chapter_id": book["chapter_id"],
                "chapter_title": book["chapter_title"],
                "chapter_file": book["chapter_file"],
            })
    return {
        "book_id": books[0]["book_id"],
        "book_title": books[0]["book_title"],
        "language_id": books[0]["language_id"],
        "chapters": chapters
    }
