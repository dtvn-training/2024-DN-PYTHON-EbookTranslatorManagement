from database.db import db
from app.models import User
from utils.hashPassword import check_password
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.interfaces import Status
from utils.token_expire_time import access_token_expiry, refresh_token_expiry


def register_service(username, password):
    is_exists = User.query.filter(User.username == username).first()
    if is_exists:
        return None, Status.DISALLOW
    user = User(username=username, user_password=password)
    db.session.add(user)
    db.session.commit()
    return user, Status.SUCCESS


def login_service(username, password):
    user = User.query.filter_by(
        username=username).first()
    if not user:
        return None
    if check_password(password, user.user_password):
        user_identity = identity(
            username=username, role_id=user.role_id, profile_id=user.profile_id, user_id=user.user_id)
        access_token = create_access_token(
            identity=user_identity, expires_delta=timedelta(hours=access_token))
        refresh_token = create_refresh_token(
            identity=user_identity, expires_delta=timedelta(days=refresh_token_expiry))
        return response_user(user_identity, access_token, refresh_token)
    return None


def identity(username, role_id, user_id, profile_id):
    return {
        "username": username,
        "role": role_id,
        "profile_id": profile_id,
        "user_id": user_id,
    }


def response_user(user, access_token, refresh_token):
    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
