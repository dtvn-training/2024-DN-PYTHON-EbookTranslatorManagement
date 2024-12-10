from dateutil import parser
from app.services.task import get_tasks


def get_tasks_controllers(key="", deadline=None, task_category_id=None):
    if deadline:
        deadline = parser.parse(deadline)
        deadline = deadline.strftime("%Y-%m-%d %H:%M:%S")
    tasks = get_tasks(key, deadline, task_category_id)
    tasks = [{
        "task_id": task[0],
        "chapter_title": task[1],
        "deadline": task[2],
        "author": task[3],
        "book_title": task[4],
        "type": task[5],
        "language": task[6],
    } for task in tasks]
    return tasks
