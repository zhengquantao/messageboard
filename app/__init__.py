from flask import Flask, make_response, jsonify

from app.config import dev
from flask_wtf.csrf import CSRFProtect

from app.extentsions import db, swagger
from app.handle_exceptions import register_error_handlers

csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(dev.Config)  # 导入配置文件
    csrf.init_app(app)
    db.init_app(app)
    swagger.init_app(app)

    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     if request.method == 'OPTIONS':
    #         response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
    #         headers = request.headers.get('Access-Control-Request-Headers')
    #         if headers:
    #             response.headers['Access-Control-Allow-Headers'] = headers
    #     return response
    register_error_handlers(app)
    from app import simple_api
    app.register_blueprint(simple_api.views.html_page)
    app.register_blueprint(simple_api.views.api)

    return app