from flask import render_template, redirect, url_for, flash, current_app
from flask_login import current_user
from . import main

@main.route('/')
def index():
    """
    首页路由：
    - 若用户已登录，重定向至学生管理页面；
    - 否则显示公共首页。
    """
    try:
        if current_user.is_authenticated:
            return redirect(url_for('student.student_list'))
    except Exception as e:
        current_app.logger.error(f"检测用户登录状态失败: {e}")
        flash("系统异常，请稍后再试")
    return render_template('main/index.html')

@main.route('/about')
def about():
    """
    关于页面：
    显示系统或团队信息，可根据需要进行扩展。
    """
    return render_template('main/about.html')