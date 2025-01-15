from app.services.book import progress_tracking_service, progress_tracking_detail_service

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
    return Response.create(True, "Get progress tracking successfully", response(progresses, total_record))


def progress_tracking_detail_controller(book_id):
    if not book_id:
        return Response.create(False, "Book id is required", None)
    if not str(book_id).isdigit():
        return Response.create(False, "Invalid book_id", None)
    book, detail = progress_tracking_detail_service(book_id)
    if detail and book:
        return Response.create(True, "Get progress tracking detail successfully", response_progress_detail(book, detail))
    return Response.create(False, "Failed to get data", None)


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
