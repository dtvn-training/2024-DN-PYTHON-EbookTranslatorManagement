from re import match

phone_number_regex = '^\+?[0-9]{7,15}$'


def phone_number_validation(phone_number):
    return match(phone_number_regex, phone_number)
