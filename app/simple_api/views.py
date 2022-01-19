# -- coding: utf-8 --
import io

from flask import Blueprint, request,  session,  send_file
from app.simple_api.implement import send_verification_code, delete_message
from app.utils import api_response, captcha_img, login_required
from flasgger import swag_from

api = Blueprint('api', __name__, url_prefix="/v1", static_folder="../../static")


@api.route("/captcha/", methods=["GET"])
@swag_from("doc/simple_api.yml")
def captcha():
    stream, code = captcha_img()
    session["captcha"] = code
    return send_file(
        io.BytesIO(stream.getvalue()),
        mimetype='image/png',
        as_attachment=False,
        attachment_filename='result.jpg'
    )


@api.route("/verification_code", methods=["POST"])
@swag_from("doc/simple_api.yml")
def verification_code():
    mobile = request.json.get("mobile")
    captcha = request.json.get("captcha")
    response = send_verification_code(request.json)
    return response


@api.route("/messages/<msg_id>", methods=["DELETE"])
@swag_from("doc/simple_api.yml")
@login_required
def del_messages(msg_id):
    user = session.get("user")
    delete_message(user, int(msg_id))
    return api_response()
