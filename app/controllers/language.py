from app.services.language import gets_service


def gets_controller():
    languages = gets_service()
    return languages
