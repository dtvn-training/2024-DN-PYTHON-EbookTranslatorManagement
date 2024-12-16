from app.models import Language


def gets_service():
    languages = Language.query.all()
    return [language.to_dict() for language in languages]
