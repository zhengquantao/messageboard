from flask import Blueprint, request, render_template, redirect, session, url_for, send_file
from sqlalchemy import or_

from app.extensions import db
from app.simple_api.implement import update_message, insert_message
from app.utils import login_required
from app.models.models import UserInfo, MessageBoard, WxInfo
from app.utils import api_response, check_email, check_phone, Redis

html_page = Blueprint('html_page', __name__, url_prefix="/views", template_folder="../../templates")


@html_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("pages/login.html")
    else:
        data_form = request.form
        mobile = data_form.get("mobile")
        captcha = data_form.get("captcha")
        verification_code = data_form.get("verification_code")
        if Redis.read(mobile) != verification_code or session.get("captcha") != captcha:
            return redirect(url_for("html_page.login"))

        user_msg = db.session.query(UserInfo).with_entities(UserInfo.username, UserInfo.id).filter(
            UserInfo.mobile == mobile).first()
        if not user_msg:
            return redirect(url_for("html_page.login"))
        session["user"] = user_msg[1]
        session["name"] = user_msg[0]
        return redirect(url_for("html_page.messages"))


@html_page.route("/messages", methods=["GET", "POST"])
@login_required
def messages():
    if request.method == "GET":
        user={"user": session.get("user"), "name": session.get("name")}
        page = request.args.get("page", default=1, type=int)
        size = request.args.get("size", default=20, type=int)
        messages = get_message_with_page(page=page, size=size)
        return render_template("pages/messages.html", user=user, messages=messages)
    else:
        user = session.get("user")
        insert_message(user, request.form.get("message"))
        return redirect(url_for("html_page.messages"))


@html_page.route("/users", methods=["GET", "POST"])
@login_required
def users():
    if request.method == "GET":
        return render_template("pages/users.html")
    else:
        data_form = request.form
        mobile = data_form.get("mobile")
        email = data_form.get("email")
        username = data_form.get("username")
        verification_code = data_form.get("verification_code")
        wx_id = session.get("wx")
        if not check_email(email) or not check_phone(mobile):
            return redirect(url_for("html_page.users"))

        if all([mobile, email, username, verification_code]):
            obj = UserInfo(mobile=mobile, email=email, username=username)
            db.session.add(obj)
            db.session.flush()
            wx_obj = db.session.query(WxInfo).filter(WxInfo.id == wx_id).first()
            wx_obj.user_id = obj.id
            db.session.commit()
            session["user"] = obj.id
            session["name"] = username
            return redirect(url_for("html_page.messages"))
        else:
            # 缺失参数
            return redirect(url_for("html_page.users"))


@html_page.route("/logout", methods=["GET"])
def logout():
    session.pop("user")
    return redirect(url_for("html_page.login"))


@html_page.route("/messages/<msg_id>", methods=["PUT"])
# @swagger.doc("simple_api.yml#/messages")
@login_required
def change_message(msg_id):
    user = session.get("user")
    update_message(user, request.form.get("message"), int(msg_id))
    return redirect(url_for("html_page.messages"))


@html_page.route("/reg/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("pages/reg.html")
    else:
        data_form = request.form
        mobile = data_form.get("mobile")
        email = data_form.get("email")
        username = data_form.get("username")
        verification_code = data_form.get("verification_code")
        if all([mobile, email, username, verification_code]):
            user_obj = db.session.query(UserInfo).filter(
                or_(UserInfo.mobile == mobile, UserInfo.email == email)).first()
            # 用户存在
            if user_obj:
                obj = UserInfo(mobile=mobile, email=email, username=username)
                db.session.add(obj)
                db.session.commit()
                return redirect(url_for("html_page.login"))

        return redirect(url_for("html_page.register"))


@html_page.route("/", methods=["GET"])
# @swagger.doc("simple_api.yml#/wx_login_callback")
def wx_login_callback():
    code = request.args.get("code")
    response = wx_login(code)
    return response


def get_message_with_page(page=1, size=20):
    #data = db.session.query(MessageBoard).offset(int(int(page)-1)*int(size)).limit(size).all()
    try:
        message = db.session.query(MessageBoard)
        data = message.filter(MessageBoard.id>=message.with_entities(MessageBoard.id).offset(int(int(page)-1)*int(size)).limit(1).first()).limit(size).all()
    except:
        data = api_response(code=404, message="Not Found")
    return data


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