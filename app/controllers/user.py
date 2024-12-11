from flask_jwt_extended import create_access_token


# tu dong tao jwt
def auto_authen_controller():
    user = {
        "username": "nguyenthanhan",
        "user_id": 1
    }
    token = create_access_token(identity=user)
    return {"access_token": token}
