from app.services.chapter import get_content_service, upload_chapter_service
from flask import request
from app.interfaces import Response
from datetime import datetime
import os
import uuid
from utils.secret import UPLOAD_FOLDER


def get_content_controller(chapter_id):
    try:
        id = int(chapter_id)
        if id <= 0:
            return None
        content = get_content_service(chapter_id)
        return content
    except:
        return None


def upload_chapter_controller():
    try:
        if not request.files:
            return Response.create(False, "The file is required to be uploaded", None)
        file = request.files["file_content"]
        # lay duoi mo rong
        extension = file.filename.split(".")[1]
        if extension not in ["txt", "docx"]:
            return Response.create(False, "Only TXT and DOCX files are allowed", None)
        # tao ten moi cho file
        new_filename = datetime.now().strftime('%Y%m%d%H%M%S') + \
            str(uuid.uuid4())[:20]+"."+extension
        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        # lay noi dung file
        content = file.read().decode('utf-8')
        file.seek(0)
        book_id = request.form.get("book_id")
        chapter_title = request.form.get("chapter_title")
        if not chapter_title or not book_id:
            return Response.create(False, "Upload chapter fail", None)
        file.save(file_path)
        upload_chapter = upload_chapter_service(
            book_id, chapter_title, new_filename, content)
        if upload_chapter:
            return Response.create(True, "Upload chapter successfully", None)
        return Response.create(False, "Upload chapter failed 1")
    except Exception as e:
        return Response.create(False, "Upload chapter failed", None)
