import re
from io import BytesIO

import redis
from flask import jsonify, session, redirect, url_for
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import string
from functools import wraps
from app.config.dev import Config


def api_response(data=None, code=0, message="ok"):
    return jsonify(code=code, message=message, data=data)


def captcha_img():

    def color1():  # 图片颜色
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    def color2():  # 字体颜色
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    num = random.sample(string.digits, 4)
    width = 240  # 宽
    height = 60  # 高
    image = Image.new("RGB", (width, height), (255, 255, 255))
    font = ImageFont.truetype("static/arial.ttf", 36)  # font对象
    draw = ImageDraw.Draw(image)  # 创建Draw对象
    for x in range(width):  # 填充像素
        # for y in range(30, random.randint(20, 40)):
        draw.point((x, 30), fill=color1())
    for w in range(4):  # 输出文字
        draw.text((60*w + 10, 10), num[w], font=font, fill=color2())
    image = image.filter(ImageFilter.DETAIL)
    stream = BytesIO()
    image.save(stream, "png")
    return stream, ''.join(num)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("html_page.login"))
        r = func(*args, **kwargs)
        return r
    return wrapper


def check_email(email):
    """
    检查邮箱
    :param email:
    :return:
    """
    if re.match(r'^[a-zA-Z1-9.]{4,19}@[a-zA-Z0-9]{2,3}.[com|gov|net]', email):
        return True
    else:
        return False


def check_phone(phone):
    """
    检查手机号
    :param phone:
    :return:
    """
    if re.match(r'^1[35678]\d{9}$', phone):
        return True
    else:
        return False


class Redis(object):

    @staticmethod
    def _get_r():
        r = redis.StrictRedis().from_url(Config.REDIS_URL)
        return r

    @classmethod
    def write(cls, key, value, expire=None):
        """
    	写入键值对
    	"""
        r = cls._get_r()
        r.set(key, value, ex=expire)

    @classmethod
    def read(cls, key):
        """
    	读取键值对内容
    	"""
        r = cls._get_r()
        value = r.get(key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hset(cls, name, key, value):
        """
    	写入hash表
    	"""
        r = cls._get_r()
        r.hset(name, key, value)

    @classmethod
    def hmset(cls, key, *value):
        """
    	读取指定hash表的所有给定字段的值
    	"""
        r = cls._get_r()
        value = r.hmset(key, *value)
        return value

    @classmethod
    def hget(cls, name, key):
        """
    	读取指定hash表的键值
    	"""
        r = cls._get_r()
        value = r.hget(name, key)
        return value.decode('utf-8') if value else value

    @classmethod
    def hgetall(cls, name):
        """
    	获取指定hash表所有的值
    	"""
        r = cls._get_r()
        return r.hgetall(name)

    @classmethod
    def delete(cls, *names):
        """
        删除一个或者多个
        """
        r = cls._get_r()
        r.delete(*names)

    @classmethod
    def hdel(cls, name, key):
        """
		删除指定hash表的键值
        """
        r = cls._get_r()
        r.hdel(name, key)

    @classmethod
    def expire(cls, name, expire=None):
        """
        设置过期时间
        """
        r = cls._get_r()
        r.expire(name, expire)