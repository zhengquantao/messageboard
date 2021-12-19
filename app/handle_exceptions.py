import jsonschema
from flask import make_response, jsonify


def register_error_handlers(app):
    @app.errorhandler(jsonschema.ValidationError)
    def handle_bad_request(e):
        print(e)
        return make_response(jsonify(code=400, message=e.schema.get("error", "参数校验错误")))
