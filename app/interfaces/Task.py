class Task:
    def __init__(self, task_id, chapter_title, deadline, type, language):
        self.task_id = task_id
        self.chapter_title = chapter_title
        self.deadline = deadline
        self.type = type
        self.language = language

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "type": self.type,
            "language": self.language
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4]).to_dict()
        return task_dict


class Task_Management(Task):
    def __init__(self, task_id, chapter_title, deadline, type, language, author):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.author = author

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "author": self.author,
            "type": self.type,
            "language": self.language
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4], task[5])
        return task_dict


class Task_Register(Task):
    def __init__(self, task_id, chapter_title, deadline, type, language, chapter_id, salary, book_title):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.chapter_id = chapter_id
        self.salary = salary
        self.book_title = book_title

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "type": self.type,
            "language": self.language,
            "chapter_id": self.chapter_id,
            "salary": self.salary,
            "book_title": self.book_title
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4], task[5], task[6], task[7])
        return task_dict


class Task_Content(Task):
    def __init__(self, task_id, chapter_title, deadline, type, language, content):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.content = content

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "type": self.type,
            "language": self.language,
            "content": self.content
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4], task[5]).to_dict()
        return task_dict


class MyTask(Task):
    def __init__(self, task_id, chapter_title, deadline, type, language, salary, status_task_id, status_task_title):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.salary = salary
        self.status_task_id = status_task_id
        self.status_task_title = status_task_title

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "type": self.type,
            "language": self.language,
            "salary": self.salary,
            "status_task_id": self.status_task_id,
            "status_task_title": self.status_task_title
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4], task[5], task[6], task[7]).to_dict()
        return task_dict


class CountAndRecord():
    def __init__(self, count, tasks):
        self.count = count
        self.tasks = tasks

    def to_dict(self):
        return {
            "count": self.count,
            "tasks": self.tasks
        }

    @classmethod
    def create(cls, count, tasks):
        count_and_record_dict = cls(count, tasks).to_dict()
        return count_and_record_dict
