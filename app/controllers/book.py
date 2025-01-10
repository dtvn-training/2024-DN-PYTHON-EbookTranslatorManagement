from app.services.book import progress_tracking_service, progress_tracking_detail_service
from collections import defaultdict
from flask import request
from app.interfaces import Response


def progress_tracking_controller():
    current_page = request.args.get("current_page", 1)
    limit = request.args.get("limit", 10)
    key = str(request.args.get("key", ""))
    language_id = request.args.get("language", None)
    if language_id:
        if not str(language_id).isdigit():
            return Response(False, "Invalid language", None)
        language_id = int(language_id)

    if not str(limit).isdigit():
        return Response.create(False, "Invalid limit", None)
    if not str(current_page).isdigit():
        return Response.create(False, "Invalid current_page", None)
    current_page = int(current_page)
    limit = int(limit)
    offset = (current_page - 1)*limit
    progresses, total_record = progress_tracking_service(
        offset, limit, key, language_id)
    if progresses is None:
        return Response.create(False, "Failed to get data", None)
    new_progress = group_books_by_id(progresses)
    return Response.create(True, "Get progress tracking successfully", response(new_progress, total_record))


def progress_tracking_detail_controller(book_id):
    if not book_id:
        return Response.create(False, "Book id is required", None)
    if not str(book_id).isdigit():
        return Response.create(False, "Invalid book_id", None)
    book, detail = progress_tracking_detail_service(book_id)
    detail = group_chapter_by_id(detail)
    if detail and book:
        return Response.create(True, "Get progress tracking detail successfully", response_progress_detail(book, detail))
    return Response.create(False, "Failed to get data", None)


# gop cac record trung chapter_id
def group_chapter_by_id(data):
    result = {}
    for item in data:
        chapter_id = item["chapter_id"]
        if not result.get(chapter_id):
            result[chapter_id] = item
            continue
        if not all([item["filename"], result[chapter_id]["filename"]]):
            continue
        if result[chapter_id]["created_at"] < item["created_at"]:
            result[chapter_id] = item
    return list(result.values())


# gop cac record co chung book_id
def group_books_by_id(data):
    result = defaultdict(
        lambda: {"book_id": "", "book_title": "", "language": "", "chapter": []})
    for item in data:
        book_id = item["book_id"]
        # neu book id chua co trong result thi them vao
        if not result[book_id]["book_id"]:
            result[book_id]["book_id"] = book_id
            result[book_id]["book_title"] = item["book_title"]
            result[book_id]["language"] = item["language"]
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


def response(progress, total_records):
    return {
        "information": progress,
        "total_records": total_records
    }


def response_progress_detail(book, details):
    return {
        "book": book,
        "details": details
    }
