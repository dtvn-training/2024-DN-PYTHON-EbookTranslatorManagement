from app.models import Chapter
from database.db import db
from utils.limitContent import limit_content


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


def upload_chapter_service(book_id, chapter_title, filename, chapter_content):
    try:
        chapter = Chapter(book_id, chapter_title, filename, chapter_content)
        db.session.add(chapter)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False
