from app.models import Content, Task, Chapter, TaskCategory
from database.db import db
from app.interfaces import Content as ContentInterface


def get_content_service(task_id):
    try:
        is_content = Content.query.filter(Content.task_id == task_id).count()
        if (is_content == 0):
            chapter = Chapter.query.filter(Task.task_id == task_id).join(
                Task, Task.chapter_id == Chapter.chapter_id
            ).join(
                TaskCategory, TaskCategory.task_category_id == Task.task_category_id
            ).with_entities(Chapter.chapter_id, TaskCategory.task_category_id).first()
            chapter_id = chapter[0]
            task_category_id = chapter[1]
            if task_category_id > 1:
                task_category_id = task_category_id - 1
            task = Chapter.query.filter(Chapter.chapter_id == chapter_id, Task.task_category_id == task_category_id).join(
                Task, Task.chapter_id == Chapter.chapter_id
            ).with_entities(Task.task_id).first()
            if not task:
                return None
            task_id = task[0]
        content = Content.query.with_entities(Content.content_id, Content.content,  Content.status).filter(Content.task_id == task_id).order_by(
            Content.created_at.desc()).first()
        if not content:
            return None
        content = ContentInterface.create(content)
        return content
    except:
        return False


def upload_content_service(task_id, content, user_id, status=False, filename=None):
    try:
        # code 1: success, code 2: dont allow to upload, code 3: failure
        code = 1
        # kiem tra xem member co phai la nguoi nhan task nay khong
        is_allowed = Task.query.filter(
            Task.task_id == task_id, Task.user_id == user_id, Task.can_do == True).count()
        if is_allowed == 0:
            code = 2
            return False, code
        content = Content(content, task_id, status, filename)
        db.session.add(content)
        db.session.commit()
        return content.to_dict(), code
    except:
        db.session.rollback()
        code = 0
        return False, code
