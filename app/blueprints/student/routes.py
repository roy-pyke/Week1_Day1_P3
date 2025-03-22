from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from app.models import Student
from app.extensions import db
from . import student


@student.route('/list', methods=['GET'])
@login_required
def student_list():
    """
    学生列表页面，展示所有学生信息。
    """
    try:
        students = Student.query.all()
    except Exception as e:
        current_app.logger.error(f"查询学生列表失败: {e}")
        flash("无法加载学生列表，请稍后再试")
        students = []
    return render_template('student/student_list.html', students=students)


@student.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    添加学生页面：
    - GET 请求返回添加页面
    - POST 请求处理添加操作，自动使用当前登录用户作为创建者
    """
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        major = request.form.get('major')

        # 验证必填信息
        if not name or not age:
            flash("请填写必要的学生信息")
            return render_template('student/add_student.html')

        try:
            # 自动设置 added_by 为当前登录用户的 id
            new_student = Student(name=name, age=int(age), added_by=current_user.id, major=major)
            db.session.add(new_student)
            db.session.commit()
            flash("学生添加成功")
            return redirect(url_for('student.student_list'))
        except Exception as e:
            current_app.logger.error(f"添加学生失败: {e}")
            db.session.rollback()
            flash(f"添加学生失败，请稍后再试: {e}")
    return render_template('student/add_student.html')


@student.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    """
    编辑学生页面：
    - GET 请求返回编辑页面
    - POST 请求处理更新操作，更新姓名、年龄、专业等信息，但不允许修改 added_by 字段
    """
    student_obj = Student.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        major = request.form.get('major')

        if not name or not age:
            flash("请填写必要的学生信息")
            return render_template('student/edit_student.html', student=student_obj)

        try:
            student_obj.name = name
            student_obj.age = int(age)
            student_obj.major = major
            # 注意：added_by 字段不允许修改
            db.session.commit()
            flash("学生信息更新成功")
            return redirect(url_for('student.student_list'))
        except Exception as e:
            current_app.logger.error(f"更新学生失败: {e}")
            db.session.rollback()
            flash("更新学生失败，请稍后再试")
    return render_template('student/edit_student.html', student=student_obj)


@student.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    """
    删除学生操作：
    通过 POST 请求删除学生信息，删除时同时移除与该学生相关的 added_by 关联
    """
    student_obj = Student.query.get_or_404(id)

    try:
        db.session.delete(student_obj)
        db.session.commit()
        flash("学生已删除")
    except Exception as e:
        current_app.logger.error(f"删除学生失败: {e}")
        db.session.rollback()
        flash("删除学生失败，请稍后再试")
    return redirect(url_for('student.student_list'))