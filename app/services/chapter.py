from app.models import Chapter
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
        chapter_dict = Content(chapter[0], chapter[1], chapter[2])
        return chapter_dict


def get_content_service(chapter_id):
    content = Chapter.query.filter(Chapter.chapter_id == chapter_id).with_entities(
        Chapter.chapter_id,
        Chapter.chapter_content,
        Chapter.filename
    ).first()
    content = Content.create(content).to_dict()
    return content
