from app.models import Content, Task, Chapter, TaskCategory, KPI
from database.db import db
from app.interfaces import Content as ContentInterface, Status
from utils.enumTaskCategory import task_category_name
from utils.difference_word import difference_word


def get_content_service(task_id):
    try:
        is_content = Content.query.filter(Content.task_id == task_id).count()
        if (is_content == 0):
            chapter = Chapter.query.filter(Task.task_id == task_id).join(
                Task, Task.chapter_id == Chapter.chapter_id
            ).join(
                TaskCategory, TaskCategory.task_category_id == Task.task_category_id
            ).with_entities(Chapter.chapter_id, TaskCategory.task_category_id).first()
            chapter_id = chapter[0]
            task_category_id = chapter[1]
            if task_category_id > 1:
                task_category_id = task_category_id - 1
            task = Chapter.query.filter(Chapter.chapter_id == chapter_id, Task.task_category_id == task_category_id).join(
                Task, Task.chapter_id == Chapter.chapter_id
            ).with_entities(Task.task_id).first()
            if not task:
                return None
            task_id = task[0]
        content = Content.query.with_entities(Content.content_id, Content.content,  Content.status).filter(Content.task_id == task_id).order_by(
            Content.created_at.desc()).first()
        if not content:
            return None
        content = ContentInterface.create(content)
        return content
    except:
        return False


def upload_content_service(task_id, content, user_id, status=False, filename=None):
    try:
        if not is_user_allowed_for_task(task_id, user_id):
            return False, Status.DISALLOW

        if status:
            result = update_task_state(task_id, user_id, content)
            if result is None:
                return None, Status.NOTFOUND
            if result.get('kpi'):
                db.session.add(result['kpi'])
        new_content = Content(content, task_id, status, filename)
        db.session.add(new_content)
        db.session.commit()

        return new_content.to_dict(), Status.SUCCESS

    except:
        return False, Status.ERROR


def is_user_allowed_for_task(task_id, user_id):
    """Check if the user is allowed to upload content for the task."""
    return Task.query.filter(Task.task_id == task_id, Task.user_id == user_id).count() > 0


def update_task_state(task_id, user_id, content):
    """Update task state based on the task category and create a KPI if necessary."""
    task = Task.query.get(task_id)
    if not task:
        return None
    kpi = None
    if task.task_category_id == task_category_name["translation"]:
        kpi = KPI(user_id, task_id, task.salary)
    else:
        task_content = get_latest_task_content(task_id)
        if not task_content:
            return None
        diff_count = difference_word(content, task_content)
        salary = diff_count * task.base_salary_multiplier
        latest_kpi = KPI.query.filter(KPI.task_id == task.task_id).order_by(
            KPI.created_at.desc()).first()
        latest_kpi.salary = latest_kpi.salary - salary
        if (latest_kpi.salary < 0):
            latest_kpi.salary = 0
        kpi = KPI(user_id, task_id, salary)

    if task.task_category_id != task_category_name["review"]:
        task.task_category_id += 1
    else:
        task.is_completed = True

    task.user_id = None
    return {"task": task, "kpi": kpi}


def get_latest_task_content(task_id):
    """Retrieve the most recent content for the given task."""
    content = Content.query.filter(Content.task_id == task_id, Content.status == True).order_by(
        Content.created_at.desc()).first()
    content = content.to_dict()
    return content["content"]
