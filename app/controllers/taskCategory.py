from app.services.taskCategory import gets as get_task_category_service


def gets():
    task_categories = get_task_category_service()
    if not task_categories:
        return None
    response = [category.to_dict() for category in task_categories]
    return response
