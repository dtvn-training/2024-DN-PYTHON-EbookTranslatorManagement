from app.models import Chapter
from utils.limitContent import limit_content
from app.interfaces import Status
from database.db import db


class Content:
    def __init__(self, chapter_id, content, filename):
        self.content = content
        self.chapter_id = chapter_id
        self.filename = filename

    def to_dict(self):
        return {
            "chapter_id": self.chapter_id,
            "content": limit_content(self.content),
            "filename": self.filename
        }

    @classmethod
    def create(cls, chapter):
        chapter_dict = cls(chapter[0], chapter[1], chapter[2])
        return chapter_dict


def get_content_service(chapter_id):
    content = Chapter.query.filter(Chapter.chapter_id == chapter_id).with_entities(
        Chapter.chapter_id,
        Chapter.chapter_content,
        Chapter.filename
    ).first()
    content = Content.create(content).to_dict()
    return content


def edit_chapter_service(chapter_id, chapter_title, chapter_content, filename, chapter_position):
    try:
        chapter = Chapter.query.filter(
            Chapter.chapter_id == chapter_id).first()
        if not chapter:
            return None, Status.NOTFOUND
        if chapter_title:
            chapter.chapter_title = chapter_title
        if chapter_content:
            chapter.chapter_content = chapter_content
            chapter.filename = filename
        if chapter_position:
            chapter_position = int(chapter_position)
            chapter.chapter_position = chapter_position
        db.session.commit()
        return chapter.to_dict(), Status.SUCCESS
    except:
        return None, Status.ERROR


def delete_chapter_service(chapter_id):
    try:
        chapter = Chapter.query.filter(
            Chapter.chapter_id == chapter_id).first()
        if not chapter:
            return None, Status.NOTFOUND
        db.session.delete(chapter)
        db.session.commit()
        return True, Status.SUCCESS
    except:
        return None, Status.ERROR
