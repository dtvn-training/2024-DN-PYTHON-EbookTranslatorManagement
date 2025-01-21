from flask import Blueprint, jsonify
from app.controllers.user import auto_authen_controller, register_controller, login_controller, edit_profile_controller, get_profile_controller
from flask_jwt_extended import jwt_required

users = Blueprint("users", __name__, url_prefix="/api/user")


# tu dong tao token de test
@users.route("/auto-authen")
def auto_authen():
    return jsonify(auto_authen_controller())


@users.route("/register", methods=['POST'])
def register():
    reister = register_controller()
    if reister["is_success"]:
        return jsonify(reister), 201
    return jsonify(reister), 400


@users.route("/login", methods=['POST'])
def login():
    login = login_controller()
    if login["is_success"]:
        return jsonify(login), 200
    return jsonify(login), 400


@users.route("/edit-profile", methods=['POST'])
@jwt_required()
def edit_profile():
    profile = edit_profile_controller()
    if profile["is_success"]:
        return jsonify(profile), 200
    return jsonify(profile), 400


@users.route("/get-profile", methods=["GET"])
@jwt_required()
def get_profile():
    profile = get_profile_controller()
    if profile["is_success"]:
        return jsonify(profile), 200
    return jsonify(profile), 400
