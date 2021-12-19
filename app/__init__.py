from flask import Flask, make_response, jsonify

from app.app import register_blueprints, register_logging, register_extensions, register_config
from app.config import dev

from app.handle_exceptions import register_error_handlers


def create_app():
    app = Flask(__name__)

    register_config(app)

    register_logging(app)

    register_extensions(app)

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
    register_blueprints(app)

    return app