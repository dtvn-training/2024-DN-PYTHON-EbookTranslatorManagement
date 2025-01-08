import bcrypt

TYPE = 'utf-8'


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(TYPE), salt)
    hashed = hashed.decode(TYPE)
    return hashed


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(TYPE), hashed.encode(TYPE))
