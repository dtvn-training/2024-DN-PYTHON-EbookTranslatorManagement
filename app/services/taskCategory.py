from app.models import TaskCategory, StatusTask


def gets():
    return TaskCategory.query.all()


def get_my_task_status_service():
    status = StatusTask.query.all()
    return [status.to_dict() for status in status]
