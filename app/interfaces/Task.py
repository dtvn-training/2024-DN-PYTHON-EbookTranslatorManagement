class Task:
    def __init__(self, task_id, chapter_title, deadline, type, language):
        self.task_id = task_id
        self.chapter_title = chapter_title
        self.deadline = deadline
        self.type = type
        self.language = language


class Task_Management(Task):
    def __init__(self, task_id, chapter_title, deadline, type, language, full_name):
        super().__init__(task_id, chapter_title, deadline, type, language)
        self.full_name = full_name

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "chapter_title": self.chapter_title,
            "deadline": self.deadline,
            "Task Owner": self.full_name,
            "type": self.type,
            "language": self.language
        }

    @classmethod
    def create(cls, task):
        task_dict = Task_Management(
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
        task_dict = Task_Register(
            task[0], task[1], task[2], task[3], task[4], task[5], task[6])
        return task_dict
