import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI") or "mysql+pymysql://root:123456@localhost:3306/messageboard?charset=utf8mb4"
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "messageboardingxxxeee"
    REDIS_URL = os.getenv("REDIS_URL") or "redis://127.0.0.1:6379/0"
    SWAGGER = {
        "doc_root": "../doc/",
        "domain": "http://127.0.0.1:5000",
        "base_url": "/",
        "swagger": "2.0",
        "info": {"version": "v1", "title": "swagger document", "description": "简单"},
        "url_prefix": "/apidoc/",
        "enable_cors": True,
        "swagger_ui": "https://petstore.swagger.io",
        "schemes": "http"
    }