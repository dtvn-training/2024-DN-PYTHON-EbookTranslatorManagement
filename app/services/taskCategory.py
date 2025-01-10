from app.models import TaskCategory

def gets():
    return TaskCategory.query.all()
