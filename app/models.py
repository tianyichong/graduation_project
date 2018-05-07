from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager


class Permission:
    ENROLL = 1
    INFORMATION = 2
    CHECK = 4
    QUERY = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    enrolment = db.Column(db.Integer, default=0)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    '''通过角色名查找现有的角色，然后再进行更新'''
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.ENROLL, Permission.INFORMATION],
            'Administrator': [Permission.ENROLL, Permission.INFORMATION, Permission.CHECK, Permission.QUERY,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Number(db.Model):
    __tablename__ = 'numbers'
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, unique=True)
    sign_point = db.Column(db.String(64), default='武邑中学')
    exam_department = db.Column(db.String(64))
    exam_type = db.Column(db.String(64), default='全国统考')

    def __repr__(self):
        return '<Number %r>' % self.num


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    number = db.Column(db.Integer, db.ForeignKey('numbers.num'))

    confirmed = db.Column(db.Boolean, default=False)   # 记录是否验证
    repeat = db.Column(db.Integer, default=0)  # 记录登录次数
    enrolment = db.Column(db.Boolean, default=False)  # 记录是否报名
    commitment = db.Column(db.Boolean, default=False)  # 记录是否遵守诚信考试

    name = db.Column(db.String(64))
    sex = db.Column(db.String(64))
    id_number = db.Column(db.Integer, unique=True)
    nation = db.Column(db.String(64))
    birthday = db.Column(db.Date)
    student_id = db.Column(db.Integer, unique=True)  # 学籍号
    native_place = db.Column(db.String(64))  # 籍贯
    student_status = db.Column(db.String(64), unique=True)
    political_status = db.Column(db.String(64))  # 政治面貌
    postal_address = db.Column(db.String(64))  # 通讯地址
    recipients = db.Column(db.String(64))    # 收件人
    contacts = db.Column(db.String(64))  # 联系人
    postal_code = db.Column(db.Integer)  # 邮编
    home_phone_number = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    high_school = db.Column(db.String(64))
    class_in_school = db.Column(db.String(64))
    graduation_category = db.Column(db.String(64))  # 毕业类别
    examinee_category = db.Column(db.String(64))  # 考生类别
    art_type = db.Column(db.String(64))  # 艺术统考类
    major = db.Column(db.String(64))  # 专业方向
    sport = db.Column(db.String(64))  # 体育专业测试
    sport_project = db.Column(db.String(64))  # 体育测试项目
    headmaster = db.Column(db.String(64))  # 班主任
    speciality = db.Column(db.String(64))  # 特长

    def __init__(self, **kwargs):
        # 定义默认的用户角色
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 获取密码散列值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成一个验证token
    def generate_confirmation_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    # 检验令牌，confirm() 方法还检查令牌中的 id 是否和存储在 current_user 中的已登录用户匹配
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 生成一个 reset_password 的 token
    def generate_reset_token(self, expiration=60):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    # 重置密码
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    # 获取更改邮箱的 token
    def generate_change_email_token(self, new_email, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    # 更改邮箱
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    '''检查用户是否有指定的权限'''
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
