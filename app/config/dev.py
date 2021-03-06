import os


class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "mysql+pymysql://root:123456@localhost:3306/messageboard?charset=utf8mb4")
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "messageboardingxxxeee"
    REDIS_URL = os.getenv("REDIS_URL", "redis://:123456@127.0.0.1:6379/0")
    SWAGGER = {
        "host": "http://127.0.0.1:5000",
        "basePath": "/",
        "paths": "../doc/",
        "swagger": "2.0",
        "info": {"version": "2.0", "title": "swagger document", "description": "简单"},
        "url_prefix": "/apidocs/",
        # "enable_cors": True,
        # "swagger_ui": "https://petstore.swagger.io",
        "schemes": ["http"]
    }