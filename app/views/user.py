from flask import Blueprint, jsonify
from app.controllers.user import auto_authen_controller

users = Blueprint("users", __name__, url_prefix="/api/user")


# tu dong tao token de test
@users.route("/auto-authen", methods=["GET"])
def auto_authen():
    return jsonify(auto_authen_controller())
