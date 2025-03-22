import os

from flask import Flask
from .extensions import db, login_manager
from . import models


def create_app(config_class='config.Config'):
    app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(app_root, 'templates')
    app = Flask(__name__, template_folder=template_dir)

    # 加载配置
    try:
        app.config.from_object(config_class)
    except Exception as e:
        raise Exception("加载配置失败: {}".format(e))

    # 初始化扩展
    try:
        db.init_app(app)
        login_manager.init_app(app)
    except Exception as e:
        raise Exception("初始化扩展失败: {}".format(e))

    # 延迟导入蓝图，避免循环引用问题
    try:
        from .blueprints.auth import auth as auth_blueprint
        from .blueprints.student import student as student_blueprint
        from .blueprints.main import main as main_blueprint

        # 注册蓝图，按需指定 URL 前缀，确保各模块相对独立
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(student_blueprint, url_prefix='/student')
        app.register_blueprint(main_blueprint)
    except Exception as e:
        raise Exception("蓝图注册失败: {}".format(e))

    return app