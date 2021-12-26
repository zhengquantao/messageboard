# -- coding: utf-8 --
import random
import string

from flask import jsonify, request, session, redirect, url_for
from sqlalchemy.sql.elements import or_
from app.extensions import db
from app.models.models import UserInfo, MessageBoard, WxInfo
from app.utils import api_response, check_email, check_phone, Redis


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
    if user_id and content:
        msg_obj = MessageBoard(user_id=user_id, content=content)
        db.session.add(msg_obj)
        db.session.commit()
    else:
        pass


def update_message(user_id, content, msg_id):
    if not (user_id and content and msg_id):
        return api_response(code=500, message="data not empty")
    msg_obj = db.session.query(MessageBoard).filter(MessageBoard.id==msg_id).first()
    if msg_obj:
        if user_id == msg_obj.user_id:
            msg_obj.content = content
            db.session.add(msg_obj)
            db.session.commit()
        else:
            pass
    else:
        pass


def delete_message(user_id, msg_id):
    if not (user_id and msg_id):
        return api_response(code=500, message="not user_id or not msg_id")
    msg_obj = db.session.query(MessageBoard).filter(MessageBoard.id == msg_id).first()
    if msg_obj:
        if user_id == msg_obj.user_id:
            db.session.delete(msg_obj)
            db.session.commit()
        else:
            pass
    else:
        pass

