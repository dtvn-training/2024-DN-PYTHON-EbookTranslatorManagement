from app.services.chapter_services import get_all_chapters as get_chapters_from_service

def get_all_chapters():
    chapters = get_chapters_from_service()
    if not chapters:
        return None
    response = [chapter.to_dict() for chapter in chapters]
    return response