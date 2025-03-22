import os
from dotenv import load_dotenv

#加载项目根目录下的 .env文件
load_dotenv()


class Config:
    # 秘钥建议通过环境变量传入，保证安全性
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

    # 数据库 URI 同样通过环境变量配置，默认使用 SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///students.db')

    # 禁用 SQLAlchemy 的事件系统，减少不必要的开销
    SQLALCHEMY_TRACK_MODIFICATIONS = False