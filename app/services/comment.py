from app.models import Comment, Task, Profile, User, Role
from app.interfaces import Comment as CommentInterface, Status
from database.db import db


def get_comments_service(task_id):
    try:
        comments = Comment.query.filter(Comment.task_id == task_id).join(
            Task, Task.task_id == Comment.task_id
        ).join(
            User, User.user_id == Comment.user_id
        ).join(
            Profile, Profile.profile_id == User.profile_id
        ).join(
            Role, User.role_id == Role.role_id
        ).with_entities(Comment.comment_id, Profile.fullname, Role.name, Comment.content, Comment.status).all()
        comments = [CommentInterface.create(comment) for comment in comments]
        if not comments:
            return None, Status.NOTFOUND
        return comments, Status.SUCCESS
    except:
        return None, Status.ERROR


def confirm_comment_service(comment_id, user_id):
    try:
        comment = Comment.query.filter(Comment.comment_id == comment_id, Task.user_id == user_id).join(
            Task, Task.task_id == Comment.task_id
        ).join(User, User.user_id == Comment.user_id).first()
        if not comment:
            return None, Status.NOTFOUND
        comment.status = True
        db.session.commit()
        return comment.to_dict(), Status.SUCCESS
    except:
        return False, Status.ERROR
