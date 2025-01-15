class Progress:
    def __init__(self, book_id, book_title, language, chapter_id, chapter_title, task_id, is_completed, category):
        self.book_id = book_id
        self.book_title = book_title
        self.language = language
        self.chapter_id = chapter_id
        self.chapter_title = chapter_title
        self.task_id = task_id
        self.is_completed = is_completed
        self.category = category

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "book_title": self.book_title,
            "language": self.language,
            "chapter_id": self.chapter_id,
            "chapter_title": self.chapter_title,
            "task_id": self.task_id,
            "is_completed": self.is_completed,
            "category": self.category,
        }

    @classmethod
    def create(cls, progress):
        progress_dict = cls(
            progress[0], progress[1], progress[2], progress[3], progress[4], progress[5], progress[6], progress[7]).to_dict()
        return progress_dict


class Book:
    def __init__(self, book_id, title, language):
        self.book_id = book_id
        self.title = title
        self.language = language

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "language": self.language,
        }

    @classmethod
    def create(cls, book):
        book_dict = cls(book[0], book[1], book[2]).to_dict()
        return book_dict


class Progress_Detail:
    def __init__(self, chapter_id, title, fullname, deadline, is_completed, task_category, filename, created_at, chapter_position):
        self.chapter_id = chapter_id
        self.title = title
        self.fullname = fullname
        self.deadline = deadline
        self.is_completed = is_completed
        self.task_category = task_category
        self.filename = filename
        self.created_at = created_at
        self.chapter_position = chapter_position

    def to_dict(self):
        return {
            "chapter_id": self.chapter_id,
            "title": self.title,
            "fullname": self.fullname,
            "deadline": self.deadline,
            "is_completed": self.is_completed,
            "task_category": self.task_category,
            "filename": self.filename,
            "created_at": self.created_at,
            "chapter_position": self.chapter_position,
        }

    @classmethod
    def create(cls, progress_detail):
        progress_detail_dict = cls(
            progress_detail[0], progress_detail[1], progress_detail[2], progress_detail[3],
            progress_detail[4], progress_detail[5], progress_detail[6], progress_detail[7], progress_detail[8]).to_dict()
        return progress_detail_dict


class ChapterProgress:
    def __init__(self, book_id, count):
        self.count = count
        self.book_id = book_id

    def to_dict(self):
        return {
            "count": self.count,
            "book_id": self.book_id,
        }

    @classmethod
    def create(cls, chapter):
        chapter_dict = cls(chapter[0], chapter[1]).to_dict()
        return chapter_dict
