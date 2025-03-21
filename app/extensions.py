from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 初始化 Flask-Login，并指定未登录用户访问时跳转的视图函数名称
login_manager = LoginManager()
login_manager.login_view = 'auth.login'