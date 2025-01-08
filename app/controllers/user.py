from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import request
from app.interfaces import Response
from utils.isValidPassword import is_valid_password
from utils.hashPassword import hash_password
from app.services.user import register_service, login_service
from app.interfaces import Status
from datetime import timedelta


# tu dong tao jwt
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


def refresh_token_controller():
    try:
        user = get_jwt_identity()
        access_token = create_access_token(
            identity=user, expires_delta=timedelta(minutes=5))
        return Response.create(True, "Refresh token successfully", access_token)
    except:
        return Response.create(False, "Fail to refresh token", None)
