from database.db import db
from app.models import User, Profile
from utils.hashPassword import check_password
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.interfaces import Status


def register_service(username, password):
    try:
        with db.session.begin():
            is_exists = User.query.filter(User.username == username).first()
            if is_exists:
                return None, Status.DISALLOW
            profile = Profile()
            user = User(username=username, user_password=password, profile_id=profile.profile_id)
            db.session.add(profile)
            db.session.add(user)
        return user, Status.SUCCESS
    except:
        db.session.rollback()  
        return None, Status.ERROR

def login_service(username, password):
    try:
        user = User.query.filter_by(
            username=username).first()
        if not user:
            return None
        if check_password(password, user.user_password):
            user_identity = identity(
                username=username, role_id=user.role_id, profile_id=user.profile_id, user_id=user.user_id)
            access_token = create_access_token(
                identity=user_identity, expires_delta=timedelta(minutes=5))
            refresh_token = create_refresh_token(
                identity=user_identity, expires_delta=timedelta(days=30))
            return response_user(username, access_token, refresh_token)
        return None
    except:
        return None


def identity(username, role_id, user_id, profile_id):
    return {
        "username": username,
        "role": role_id,
        "profile_id": profile_id,
        "user_id": user_id,
    }


def response_user(username, access_token, refresh_token):
    return {
        "username": username,
        "access_token": access_token,
        "refresh_token": refresh_token
    }
