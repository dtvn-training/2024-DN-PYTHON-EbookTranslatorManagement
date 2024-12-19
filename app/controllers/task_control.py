from app.services.task_services import create_task as create_task_from_services
from datetime import datetime

def parse_datetime(date_string):
    formats = "%a, %d %b %Y %H:%M:%S GMT"

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue

    raise ValueError(f"Invalid datetime format: {date_string}")

def create_task(data):
    results = []

    if not data:
        raise ValueError("Query has problem.")

    for task in data:
        chapter_id = task.get('chapter_id')
        deadline_str = task.get('deadline')
        salary = task.get('salary')

        if not chapter_id or not deadline_str or not salary:
            results.append({"error": f"Missing fields for chapter_id {chapter_id or 'unknown'}"})
            continue

        try:
            deadline = parse_datetime(deadline_str)
        except ValueError as e:
            results.append({"error": f"Invalid deadline format for chapter_id {chapter_id}: {e}"})
            continue

        new_task = create_task_from_services(chapter_id, deadline, salary, category_id=1)

        if not new_task:
            results.append({"error": f"Failed to create task for chapter_id {chapter_id}"})
        else:
            results.append(new_task.to_dict())
            
    return results



