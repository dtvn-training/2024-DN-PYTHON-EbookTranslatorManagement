from app.models import Chapter

def get_all_chapters():
    chapters = Chapter.query.all()
    return chapters