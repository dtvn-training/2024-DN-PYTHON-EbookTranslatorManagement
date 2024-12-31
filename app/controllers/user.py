from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import request
from app.interfaces import Response, Status
from utils import is_valid_password, hash_password, phone_number_validation, email_validation, random_file_name, UPLOAD_FOLDER
from app.services.user import register_service, login_service, edit_profile_service, get_profile_service
import os


def auto_authen_controller():
    user = {
        "username": "john_doe",
        "user_id": 5
    }
    token = create_access_token(identity=user)
    return {"access_token": token}


def register_controller():
    try:
        res_json = request.get_json()
        username = res_json.get('username', "")
        password = res_json.get("password", "")
        confirm_password = res_json.get("confirm_password", "")
        if not username or not password:
            return Response.create(False, "Invalid username or password", None)
        if password != confirm_password:
            return Response.create(False, "Passwords do not match", None)
        if not is_valid_password(password):
            return Response.create(False, "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character", None)
        password = hash_password(password)
        register, status = register_service(username, password)
        if register:
            return Response.create(True, "Register successfully", None)
        if status == Status.ERROR:
            return Response.create(False, "Fail to register", None)
        return Response.create(False, "Username already exists", None)
    except:
        return Response.create(False, "Fail to register", None)


def login_controller():
    try:
        res_json = request.get_json()
        username = res_json.get('username', "")
        password = res_json.get("password", "")
        if not username or not password:
            return Response.create(False, "Invalid username or password", None)
        user = login_service(username, password)
        if user:
            return Response.create(True, "Login successfully", user)
        return Response.create(False, "Invalid username or password", None)
    except:
        return Response.create(False, "Fail to login", None)


def edit_profile_controller():
    user = get_jwt_identity()
    if not user:
        return Response.create(False, "User not authenticated", None)
    profile_id = user['profile_id']
    if not profile_id:
        return Response.create(False, "Profile ID not found", None)
    fullname = request.form.get("fullname", "")
    email = request.form.get("email", "")
    phone_number = request.form.get('phone_number', "")
    avatar = request.files.get('avatar')
    file_name, status = save_avatar(avatar)
    if status == Status.DISALLOW:
        return Response.create(False, "Invalid avatar format", None)
    if not email_validation(email) and email:
        return Response.create(False, "Invalid email format", None)
    if not phone_number_validation(phone_number) and phone_number:
        return Response.create(False, "Invalid phone number format", None)
    profile, status = edit_profile_service(
        profile_id, fullname, email, phone_number, file_name)
    if profile:
        return Response.create(True, "Edit profile successfully", profile)
    if status == Status.NOTFOUND:
        return Response.create(False, "User not found", None)
    return Response.create(False, "Fail to edit profile", None)


def save_avatar(avatar_file):
    if not avatar_file:
        return None, Status.NOTFOUND
    allow_extensions = ['jpg', 'png', "jpeg"]
    extension = avatar_file.filename.split('.')[1]
    if extension not in allow_extensions:
        return None, Status.DISALLOW
    file_name = random_file_name(extension)
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    avatar_file.save(file_path)
    return file_name, Status.SUCCESS


def get_profile_controller():
    user = get_jwt_identity()
    if not user:
        return Response.create(False, "User not authenticated", None)
    profile_id = user['profile_id']
    if not profile_id:
        return Response.create(False, "Profile ID not found", None)
    profile, status = get_profile_service(profile_id)
    if profile:
        return Response.create(True, "Get profile successfully", profile)
    if status == Status.NOTFOUND:
        return Response.create(False, "User not found", None)
    return Response.create(False, "Fail to get profile", None)
