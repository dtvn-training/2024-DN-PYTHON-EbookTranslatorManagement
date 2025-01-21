from database.db import db
from app.models import User, Profile, Level
from utils.hashPassword import check_password
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from app.interfaces import Status, Profile as ProfileInterface


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
            identity=user_identity, expires_delta=timedelta(days=5))
        refresh_token = create_refresh_token(
            identity=user_identity, expires_delta=timedelta(days=30))
        return response_user(username, access_token, refresh_token)
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


def edit_profile_service(profile_id, fullname, email, phone_number, file_name):
    profile = Profile.query.filter(
        Profile.profile_id == profile_id).first()
    if not profile:
        return None, Status.NOTFOUND
    profile.fullname = fullname
    profile.email = email
    profile.phone = phone_number
    profile.avatar = file_name
    db.session.commit()
    return profile.to_dict(), Status.SUCCESS


def get_profile_service(profile_id):
    profile = Profile.query.filter(Profile.profile_id == profile_id).join(
        User, Profile.profile_id == User.profile_id
    ).join(
        Level, Level.level_id == Profile.level_id
    ).with_entities(Profile.fullname, User.username, Profile.avatar, Profile.email, Profile.phone, Level.level_type, Profile.task_quantity, User.created_at).first()
    if not profile:
        return None, Status.NOTFOUND
    profile_dict = ProfileInterface.create(profile)
    return profile_dict, Status.SUCCESS
