# -- coding: utf-8 --
import random
import string

from flask import jsonify, request, session, redirect, url_for
from sqlalchemy.sql.elements import or_
from app.extentsions import db
from app.models.models import UserInfo, MessageBoard, WxInfo
from app.utils import api_response, check_email, check_phone, Redis


def verify_login(data_form):
    mobile = data_form.get("mobile")
    captcha = data_form.get("captcha")
    verification_code = data_form.get("verification_code")
    if Redis.read(mobile) != verification_code:
        return redirect(url_for("html_page.login"))
    if session.get("captcha") != captcha:
        return redirect(url_for("html_page.login"))
    user_msg = db.session.query(UserInfo).with_entities(UserInfo.username, UserInfo.id).filter(
        UserInfo.mobile == mobile).first()
    if not user_msg:
        return redirect(url_for("html_page.login"))
    session["user"] = user_msg[1]
    session["name"] = user_msg[0]
    return redirect(url_for("html_page.messages"))


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


def get_message_with_page(page=1, size=20):
    #data = db.session.query(MessageBoard).offset(int(int(page)-1)*int(size)).limit(size).all()
    try:
        message = db.session.query(MessageBoard)
        data = message.filter(MessageBoard.id>=message.with_entities(MessageBoard.id).offset(int(int(page)-1)*int(size)).limit(1).first()).limit(size).all()
    except:
        data = api_response(code=404, message="Not Found")
    return data


def get_message_by_user(user):
    pass


def insert_message(user_id, content):
    if user_id and content:
        msg_obj = MessageBoard(user_id=user_id, content=content)
        db.session.add(msg_obj)
        db.session.commit()
    else:
        pass


def update_message(user_id, content, msg_id):
    if user_id and content and msg_id:
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
    else:
        pass


def delete_message(user_id, msg_id):
    if user_id and msg_id:
        msg_obj = db.session.query(MessageBoard).filter(MessageBoard.id == msg_id).first()
        if msg_obj:
            if user_id == msg_obj.user_id:
                db.session.delete(msg_obj)
                db.session.commit()
            else:
                pass
        else:
            pass
    else:
        pass


def register_user(data_form):
    mobile = data_form.get("mobile")
    email = data_form.get("email")
    username = data_form.get("username")
    verification_code = data_form.get("verification_code")
    if not check_email(email):
        pass
    if not check_phone(mobile):
        pass
    if all([mobile, email, username, verification_code]):
        user_obj = db.session.query(UserInfo).filter(or_(UserInfo.mobile==mobile, UserInfo.email==email)).first()
        # 用户存在
        if user_obj:
            redirect(url_for("html_page.register"))
        else:
            obj = UserInfo(mobile=mobile, email=email, username=username)
            db.session.add(obj)
            db.session.commit()
            return redirect(url_for("html_page.login"))
    else:
        # 缺失参数
        redirect(url_for("html_page.register"))


def wx_login(code):
    if code:
        wx_obj = db.session.query(WxInfo).filter(WxInfo.wx_code==code).first()
        # 不存在增加用户
        if not wx_obj:
            wx_obj = WxInfo(wx_code=code)
            db.session.add(wx_obj)
            db.session.commit()
        if not wx_obj.user_id:
            # 补充完整信息
            session["wx"] = wx_obj.id
            return redirect(url_for("html_page.users"))
        session["user"] = wx_obj.id
        session["name"] = wx_obj.user
        return redirect(url_for("html_page.messages"))
    else:
        return redirect(url_for("html_page.login"))


def perfect_user(data_form):
    mobile = data_form.get("mobile")
    email = data_form.get("email")
    username = data_form.get("username")
    verification_code = data_form.get("verification_code")
    wx_id = session.get("wx")
    if not check_email(email):
        return redirect(url_for("html_page.users"))
    if not check_phone(mobile):
        return redirect(url_for("html_page.users"))
    if all([mobile, email, username, verification_code]):
        obj = UserInfo(mobile=mobile, email=email, username=username)
        db.session.add(obj)
        db.session.flush()
        wx_obj = db.session.query(WxInfo).filter(WxInfo.id==wx_id).first()
        wx_obj.user_id = obj.id
        db.session.commit()
        session["user"] = obj.id
        session["name"] = username
        return redirect(url_for("html_page.messages"))

    else:
        # 缺失参数
        return redirect(url_for("html_page.users"))