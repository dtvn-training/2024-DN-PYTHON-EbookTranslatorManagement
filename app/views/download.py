from flask import Blueprint, send_from_directory, send_file
import os

downloads = Blueprint("downloads", __name__, url_prefix="/api/files")

# download noi dung cua files (vd: chapter)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static', 'documents')


@downloads.route("/<file_name>")
def download(file_name):
    return send_from_directory(STATIC_FOLDER, file_name, as_attachment=True)


@downloads.route("/show/<file_name>", methods=["GET"])
def show_image(file_name):
    file_path = os.path.join(STATIC_FOLDER, file_name)
    return send_file(file_path)
