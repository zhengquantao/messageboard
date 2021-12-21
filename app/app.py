
def register_config(app, param=None):
    from app.config import dev
    app.config.from_object(dev.Config)  # 导入配置文件
    

def register_extensions(app, param=None):
    """
    :param app:
    :return:
    """
    from app.extensions import db, csrf
    csrf.init_app(app)
    db.init_app(app)
    # swagger.init_app(app)


def register_logging(app, param=None):
    """
    注册日志
    :param app:
    :param params:
    :return:
    """
    import logging
    from logging.handlers import RotatingFileHandler
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    # 给处理器设置输出格式
    console_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s [%(pathname)s %(lineno)d] - %(message)s')
    console_handler.setFormatter(console_formatter)

    # 日志器添加处理器
    app.logger.addHandler(console_handler)

    # 创建文件处理器
    file_handler = RotatingFileHandler(filename='flask.log', maxBytes=100 * 1024 * 1024,
                                       backupCount=10)  # 转存文件处理器  当达到限定的文件大小时, 可以将日志转存到其他文件中

    # 日志器添加处理器
    app.logger.addHandler(file_handler)


def register_blueprints(app, param=None):
    """
    注册蓝图
    :param app: flask app
    :param params:
    :return:
    """
    from app import simple_api
    app.register_blueprint(simple_api.views.api)
    app.register_blueprint(simple_api.views.html_page)
