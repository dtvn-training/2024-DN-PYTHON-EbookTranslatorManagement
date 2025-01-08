from functools import wraps
from flask_jwt_extended import get_jwt, jwt_required
from flask import jsonify
from app.interfaces.Response import Response


def role_required(required_roles):

    def decorator(func):
        @wraps(func)
        @jwt_required()  # Bắt buộc người dùng phải có token
        def wrapper(*args, **kwargs):
            # Lấy thông tin từ token
            claims = get_jwt()
            user = claims.get('sub', None)
            if user:
                user_role = int(user["role"])
            if user_role not in required_roles:
                return jsonify(Response.create(False, "Access denied, insufficient role", None)), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
