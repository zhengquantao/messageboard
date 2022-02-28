import jsonschema
from flask import make_response, jsonify


def register_error_handlers(app):
    @app.errorhandler(jsonschema.ValidationError)
    def handle_bad_request(e):
        print(e)
        return make_response(jsonify(code=400, message=e.schema.get("error", "参数校验错误")))

    @app.errorhandler(401)
    def handle_bad_request(e):
        print(e)
        return make_response(jsonify(code=400, message="未登录"))

    @app.errorhandler(404)
    def handle_bad_request(e):
        print(e)
        return make_response(jsonify(code=404, message="页面不存在"))
