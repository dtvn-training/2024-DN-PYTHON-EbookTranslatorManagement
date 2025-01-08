import re

# Password phai co ky tu hoa, thuong, so, ky tu dac biet va toi thieu 8 ky tu
password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


def is_valid_password(password):
    return re.match(password_regex, password) is not None
