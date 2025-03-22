from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event
from .extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(150))
    # 通过 added_by 字段记录添加该学生的 User 的 id
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # 建立与 User 的关系，方便通过 user.students_added 访问当前用户添加的学生
    user = db.relationship('User', backref=db.backref('students_added', lazy=True))

    def __init__(self, name, age, added_by, major=None):
        self.name = name
        self.age = age
        self.major = major
        # 支持传入 User 对象或者直接传入 User 的 id
        self.added_by = added_by.id if hasattr(added_by, 'id') else added_by

    def __repr__(self):
        return f'<Student {self.name}>'


# 监听 added_by 属性的修改事件，确保一旦设置后就不允许修改
@event.listens_for(Student.added_by, 'set', retval=True, active_history=True)
def prevent_added_by_update(target, value, oldvalue, initiator):
    # 如果对象还没有持久化（target.id is None），允许赋值
    if target.id is None:
        return value
    # 对于已经持久化的对象，oldvalue 非空且与新值不同时禁止修改
    if oldvalue is not None and oldvalue != value:
         raise ValueError("The 'added_by' field is immutable and cannot be modified once set.")
    return value