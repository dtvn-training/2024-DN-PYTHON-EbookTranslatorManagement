from flask import Blueprint, send_from_directory
import os

downloads = Blueprint("downloads", __name__, url_prefix="/api/files")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static', 'documents')

@downloads.route("/<file_name>", methods=["GET"])
def download(file_name):
    return send_from_directory(STATIC_FOLDER, file_name, as_attachment=True)
