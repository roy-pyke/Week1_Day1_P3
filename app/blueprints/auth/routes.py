from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.extensions import db
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录页面：
    - GET 请求返回登录页面
    - POST 请求处理登录逻辑，包括表单验证、用户查询和密码校验
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 验证必填项
        if not username or not password:
            flash("请填写用户名和密码")
            return render_template('auth/login.html')

        try:
            user = User.query.filter_by(username=username).first()
        except Exception as e:
            current_app.logger.error(f"查询用户失败: {e}")
            flash("系统错误，请稍后再试")
            return render_template('auth/login.html')

        # 校验密码并登录
        if user and user.check_password(password):
            login_user(user)
            flash("登录成功")
            return redirect(url_for('student.student_list'))
        else:
            flash("用户名或密码错误")
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    """
    用户登出操作：
    退出当前登录状态，并返回登录页面
    """
    logout_user()
    flash("您已成功登出")
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    用户注册页面（可选）：
    - GET 请求返回注册页面
    - POST 请求处理注册逻辑，包括重复用户名检测与数据库写入
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 验证必填项
        if not username or not password:
            flash("请填写用户名和密码")
            return render_template('auth/register.html')

        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash("该用户名已被注册")
            return render_template('auth/register.html')

        try:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            flash("注册成功，请登录")
            return redirect(url_for('auth.login'))
        except Exception as e:
            current_app.logger.error(f"用户注册失败: {e}")
            db.session.rollback()
            flash("注册失败，请稍后再试")
    return render_template('auth/register.html')