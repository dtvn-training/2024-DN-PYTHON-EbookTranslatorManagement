from app.services.task_services import create_task as create_task_from_services 

def create_task(data):
    chapter_id = data.get('chapter_id')
    deadline = data.get('deadline')
    user_id = data.get('user_id')
    task_category = data.get('task_category')
    is_completed = data.get('is_completed')

    # Call the service layer to create the book
    new_task = create_task_from_services(chapter_id, deadline, user_id, task_category, is_completed)
    
    # Return a dictionary representation of the new book
    return new_task.to_dict(), None

