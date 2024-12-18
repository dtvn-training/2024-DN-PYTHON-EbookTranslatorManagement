from app.services.task_services import create_task as create_task_from_services
from datetime import datetime

def parse_datetime(date_string):
    formats = [
        "%a, %d %b %Y %H:%M:%S GMT",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid datetime format: {date_string}")

def create_task(data):
    chapter_id = data.get('chapter_id')
    deadline_str = data.get('deadline')
    salary = data.get('salary')
    category_id = 1

    try:
        deadline = parse_datetime(deadline_str)
    except ValueError as e:
        return None, f"Invalid deadline format: {e}"

    new_task = create_task_from_services(chapter_id, deadline, salary, category_id)
    if not new_task:
        return None, "An error occurred while creating the task."
    
    return new_task, None



