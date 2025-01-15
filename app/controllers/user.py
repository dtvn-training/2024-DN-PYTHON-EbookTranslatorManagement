from flask_jwt_extended import create_access_token


def auto_authen_controller():
    user = {
        "username": "john_doe",
        "user_id": 5
    }
    token = create_access_token(identity=user)
    return {"access_token": token}
