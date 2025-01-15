from app.models import Book, Chapter, Task, Language, TaskCategory, User, Profile, Content
from app.interfaces import Progress, Book as BookInterface, Progress_Detail, ChapterProgress
from sqlalchemy import func
from collections import defaultdict


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
        chapters = Chapter.query.filter(Chapter.book_id.in_(
            book_ids)).group_by(Chapter.book_id).with_entities(Chapter.book_id, func.count(Chapter.book_id).label("count")).all()
        chapters = [ChapterProgress.create(chapter) for chapter in chapters]
        progress = group_books_by_id(progress, chapters)
        return progress, total_record
    except Exception:
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


def progress_tracking_detail_service(book_id):
    try:
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
        progress = group_chapter_by_id(progress)
        return book, progress
    except:
        return None


def group_chapter_by_id(data):
    result = {}

    for item in data:
        chapter_id = item["chapter_id"]
        # Kiểm tra xem chapter_id đã tồn tại trong result chưa
        if not result.get(chapter_id):
            result[chapter_id] = item
            continue
        # Bỏ qua nếu thiếu `filename` trong bất kỳ bản ghi nào
        if not all([item["filename"], result[chapter_id]["filename"]]):
            continue
        # Cập nhật bản ghi nếu thời điểm tạo `created_at` mới hơn
        if result[chapter_id]["created_at"] < item["created_at"]:
            result[chapter_id] = item
    # Trả về danh sách các bản ghi đã được nhóm
    return list(result.values())


def group_books_by_id(data, chapters):
    result = defaultdict(
        lambda: {"book_id": "", "book_title": "", "language": "", "chapter": []})
    for item in data:
        book_id = item["book_id"]
        # neu book id chua co trong result thi them vao
        if not result[book_id]["book_id"]:
            result[book_id]["book_id"] = book_id
            result[book_id]["book_title"] = item["book_title"]
            result[book_id]["language"] = item["language"]
            result[book_id]["total_chapter"] = get_count_by_book_id(
                book_id, chapters)
        # loc ra cac chapter chua duoc tao task
        if not item["task_id"]:
            continue
        result[book_id]["chapter"].append({
            "category": item["category"],
            "is_completed": item["is_completed"],
            "task_id": item["task_id"],
            "chapter_id": item["chapter_id"],
            "chapter_title": item["chapter_title"],
        })

    return list(result.values())


def get_count_by_book_id(book_id, chapters):
    for chapter in chapters:
        if chapter["book_id"] == book_id:
            return chapter["count"]
        

