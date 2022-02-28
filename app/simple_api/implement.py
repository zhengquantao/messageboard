# -- coding: utf-8 --
import random
import string

from flask import jsonify, request, session, redirect, url_for
from app.extensions import db
from app.models.models import MessageBoard
from app.sql import query_one, general_edit, general_create
from app.utils import api_response, Redis


def send_verification_code(data_json):
    mobile = data_json.get("mobile")
    captcha = data_json.get("captcha")
    email = data_json.get("email")
    if session.get("captcha") != captcha:
        return api_response(code=403, message="验证码不正确")
    verification_code = ''.join(random.sample(string.digits, 4))
    # session["verification_code"] = verification_code
    Redis.write(mobile, verification_code, 300)
    return api_response(data=verification_code)


def insert_message(user_id, content):
    if not (user_id and content):
        return
    general_create(MessageBoard, {"user_id": user_id, "content": content})
    db.session.commit()


def update_message(user_id, content, msg_id) -> None:
    if not (user_id and content and msg_id):
        return api_response(code=500, message="data not empty")
    msg_obj = query_one(MessageBoard, {"id": msg_id, "user_id": user_id})
    if msg_obj:
        return api_response(code=404, message="not found")
    general_edit(msg_obj, {"content": content})
    db.session.commit()


def delete_message(filters: dict) -> jsonify:
    msg_obj = query_one(MessageBoard, filters)
    if not msg_obj:
        return api_response(code=404, message="not found")
    db.session.delete(msg_obj)
    db.session.commit()
    return api_response()


