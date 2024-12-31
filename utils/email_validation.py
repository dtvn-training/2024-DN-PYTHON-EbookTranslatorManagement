from re import match

email_regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def email_validation(email):
    return match(email_regex, email)
