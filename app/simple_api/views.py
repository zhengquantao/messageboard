# -- coding: utf-8 --
import io

from flask import Blueprint, request,  session,  send_file
# from app.extensions import swagger
from app.simple_api.implement import send_verification_code, delete_message
from app.utils import captcha_img, login_required


api = Blueprint('api', __name__, url_prefix="/v1", static_folder="../../static")


@api.route("/captcha/", methods=["GET"])
# @swagger.doc("simple_api.yml#/captcha")
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
# @swagger.doc("simple_api.yml#/verification_code")
def verification_code():
    return send_verification_code(request.json)


@api.route("/messages/<int:msg_id>", methods=["DELETE"])
# @swagger.doc("simple_api.yml#/del_message")
@login_required
def del_messages(msg_id):
    filters = {
        "user_id": session.get("user"),
        "id": msg_id,
    }
    return delete_message(filters)
