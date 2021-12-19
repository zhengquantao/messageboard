# -- coding: utf-8 --
import time

from flask import Blueprint, request, render_template, redirect, session, url_for
from app.extensions import swagger
from app.simple_api.implement import send_verification_code, get_message_with_page, insert_message, update_message, \
    delete_message, register_user, verify_login, perfect_user, wx_login
from app.utils import api_response, captcha_img, login_required


api = Blueprint('api', __name__, url_prefix="/v1", static_folder="../../static")

html_page = Blueprint('html_page', __name__, url_prefix="/", template_folder="../../templates")


@html_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["captcha"] = captcha_img()
        img = "/v1/static/captcha/code.jpg?" + str(int(time.time()))
        return render_template("pages/login.html", img=img)
    else:
        return verify_login(request.form)


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
        session["captcha"] = captcha_img()
        return render_template("pages/users.html", img="/v1/static/captcha/code.jpg")
    else:
        response = perfect_user(request.form)
        return response


@html_page.route("/logout", methods=["GET"])
def logout():
    session.pop("user")
    return redirect(url_for("html_page.login"))


@html_page.route("/messages/<msg_id>", methods=["PUT"])
@swagger.doc("simple_api.yml#/messages")
@login_required
def change_message(msg_id):
    user = session.get("user")
    update_message(user, request.form.get("message"), int(msg_id))
    return redirect(url_for("html_page.messages"))


@html_page.route("/reg/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        session["captcha"] = captcha_img()
        img = "/v1/static/captcha/code.jpg?"+str(int(time.time()))
        return render_template("pages/reg.html", img=img)
    else:
        data_form = request.form
        register_user(data_form)
        return redirect(url_for("html_page.login"))


@api.route("/captcha/", methods=["GET"])
@swagger.doc("simple_api.yml#/captcha")
def captcha():
    session["captcha"] = captcha_img()
    return api_response()


@api.route("/verification_code", methods=["POST"])
@swagger.doc("simple_api.yml#/verification_code")
def verification_code():
    mobile = request.json.get("mobile")
    captcha = request.json.get("captcha")
    response = send_verification_code(request.json)
    return response


@api.route("/messages/<msg_id>", methods=["DELETE"])
@swagger.doc("simple_api.yml#/del_message")
@login_required
def del_messages(msg_id):
    user = session.get("user")
    delete_message(user, int(msg_id))
    return api_response()


@html_page.route("/", methods=["GET"])
@swagger.doc("simple_api.yml#/wx_login_callback")
def wx_login_callback():
    code = request.args.get("code")
    response = wx_login(code)
    return response
