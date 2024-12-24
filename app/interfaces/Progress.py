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
