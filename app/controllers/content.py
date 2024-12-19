from flask import request
from app.interfaces import Response, Status
import uuid
import os
from utils.secret import UPLOAD_FOLDER
from datetime import datetime
from app.services.content import upload_content_service, get_content_service
from flask_jwt_extended import get_jwt_identity
from utils.enumTaskCategory import task_category_name


def get_content_controller(task_id):
    try:
        if not task_id:
            return Response.create(False, "Missing task_id.", None)
        if not str(task_id).isdigit():
            return Response.create(False, "Invalid task_id. It must be a valid integer.", None)

        content = get_content_service(task_id)
        if content:
            return Response.create(True, "Success to get content", content)
        return Response.create(True, "Content not found", None)
    except:
        return Response.create(False, "Fail to get content", None)


def upload_content_controller():
    try:
        task_id = request.form.get("task_id", "")
        content = request.form.get("content", "")
        status = request.form.get("status", "") == "true"
        file_content = ""
        user = get_jwt_identity()
        if not task_id:
            return Response.create(False, "Missing task_id.", None)
        if not task_id.isdigit():
            return Response.create(False, "Invalid task_id. It must be a valid integer.", None)
        task_id = int(task_id)
        # tao ten file de luu
        file_name = datetime.now().strftime('%Y%m%d%H%M%S') + \
            str(uuid.uuid4())[:20]
        if request.files:
            file_content = request.files.get("file_content")

        # khong upload dong thoi vua content vua file chua content
        if file_content and content:
            return Response.create(False, "Dont upload content and file content in a transaction", None)
        # neu content tai len o dang file thi lay content va luu file
        if file_content:
            extension = file_content.filename.split(".")[1]
            if extension not in ["txt", "docx"]:
                return Response.create(False, "Only TXT and DOCX files are allowed", None)
            file_name = file_name+"."+extension
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            # doc noi dug file
            content = file_content.read().decode('utf-8')
            file_content.seek(0)
            file_content.save(file_path)
        else:
            # neu content tai len o dang text thi tao file va luu
            file_name = file_name+".txt"
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            # tao file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        upload_content, code = upload_content_service(
            task_id, content, user["user_id"], status, file_name)
        if upload_content:
            return Response.create(True, "Upload successfully", upload_content)
        if code == Status.ERROR:
            return Response.create(False, "Upload translation failed", None)
        return Response.create(False, "Task not found or you are not authorized to upload translation for this task", None)
    except:
        return Response.create(False, "Upload translation failed", None)
