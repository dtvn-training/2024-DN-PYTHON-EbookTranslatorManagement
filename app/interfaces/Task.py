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
    def __init__(self, task_id, chapter_title, deadline, type, language, chapter_id, salary):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.chapter_id = chapter_id
        self.salary = salary

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "type": self.type,
            "language": self.language,
            "chapter_id": self.chapter_id,
            "salary": self.salary
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4], task[5], task[6])
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
    def __init__(self, task_id, chapter_title, deadline, type, language, salary):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.salary = salary

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "type": self.type,
            "language": self.language,
            "salary": self.salary
        }

    @classmethod
    def create(cls, task):
        task_dict = cls(
            task[0], task[1], task[2], task[3], task[4], task[5]).to_dict()
        return task_dict
