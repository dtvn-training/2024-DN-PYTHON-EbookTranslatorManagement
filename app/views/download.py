from flask import Blueprint, send_from_directory

downloads = Blueprint("downloads", __name__, url_prefix="/api/files")


# download noi dung cua files (vd: chapter)
@downloads.route("/<file_name>", methods=["GET"])
def download(file_name):
    return send_from_directory("static/documents", file_name, as_attachment=True)
