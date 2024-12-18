from app.models import Comment, Task, Profile, User
from app.interfaces import Comment as CommentInterface


def get_comments_service(task_id):
    # code 1: success, code 2: dont find comment, code 3: error
    try:
        code = 1
        comments = Comment.query.filter(Task.task_id == task_id).join(
            Task, Task.task_id == Comment.task_id
        ).join(
            User, User.user_id == Comment.user_id
        ).join(
            Profile, Profile.profile_id == User.profile_id
        ).with_entities(Comment.comment_id, Profile.fullname, User.role, Comment.content, Comment.status).all()
        comments = [CommentInterface.create(comment) for comment in comments]
        if not comments:
            code = 2
            return None, code
        return comments, code
    except:
        code = 3
        return None, code
