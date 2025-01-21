from app.interfaces import Response
from flask import jsonify
from werkzeug.exceptions import HTTPException, BadRequest


def error_handler(error):
    code = BadRequest.code
    message = ""
    if isinstance(error, HTTPException):
        code = error.code
        message = error.description
    else:
        message = str(error)
    response = Response.create(False, message, None)
    return jsonify(response), code
