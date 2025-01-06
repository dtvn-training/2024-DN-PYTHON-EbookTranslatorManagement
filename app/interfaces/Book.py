class Book:
    def __init__(self, book_id, language_id, book_title, chapter_id, chapter_title, chapter_file):
        self.book_id = book_id
        self.language_id = language_id
        self.book_title = book_title
        self.chapter_id = chapter_id
        self.chapter_title = chapter_title
        self.chapter_file = chapter_file

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "language_id": self.language_id,
            "book_title": self.book_title,
            "chapter_id": self.chapter_id,
            "chapter_title": self.chapter_title,
            "chapter_file": self.chapter_file
        }

    @classmethod
    def create(cls, book):
        book_dict = cls(book[0], book[1], book[2],
                        book[3], book[4], book[5]).to_dict()
        return book_dict
