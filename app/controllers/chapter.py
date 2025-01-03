from app.services.chapter import get_content_service, edit_chapter_service
from flask import request
from app.interfaces import Status, Response
from utils.content_file_type import allow_extension
from datetime import datetime
import uuid
import os
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


def edit_chapter_controller(chapter_id):
    if not chapter_id:
        return Response.create(False, "Chapter_id is required", None)
    if not str(chapter_id).isdigit():
        return Response.create(False, "Invalid chapter_id", None)
    chapter_title = request.form.get("chapter_title", "")
    chapter_position = request.form.get("chapter_position", "")
    content = ""
    new_filename = ""
    if request.files:
        file = request.files["file_content"]
        if not file:
            return Response.create(False, "The file is required to be uploaded", None)
        content, new_filename = get_content(file)
    if chapter_position and not str(chapter_position.isdigit()):
        return Response.create(False, "Invalid chapter position", None)
    chapter, status = edit_chapter_service(
        chapter_id, chapter_title, content, new_filename, chapter_position)
    if chapter:
        return Response.create(True, "Edit chapter success", chapter)
    if status == Status.NOTFOUND:
        return Response.create(False, "Chapter not found", None)
    return Response.create(False, "Edit chapter failed", None)


def get_content(file):
    extension = file.filename.split(".")[1]
    if extension not in allow_extension:
        return Response.create(False, "Only TXT and DOCX files are allowed", None)
    new_filename = datetime.now().strftime('%Y%m%d%H%M%S') + \
        str(uuid.uuid4())[:20]+"."+extension
    file_path = os.path.join(UPLOAD_FOLDER, new_filename)
    content = file.read().decode("utf-8")
    print(content)
    file.seek(0)
    # fix save file(van chua luu file duoc)
    file.save(file_path)
    return content, new_filename
