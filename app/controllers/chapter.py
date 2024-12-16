from app.services.chapter import get_content_service


def get_content_controller(chapter_id):
    try:
        id = int(chapter_id)
        if id <= 0:
            return None
        content = get_content_service(chapter_id)
        return content
    except:
        return None
