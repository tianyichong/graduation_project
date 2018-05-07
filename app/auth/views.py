from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordRequestForm, \
    ChangePasswordForm, ChangeEmailForm
from .. import db
from ..models import User, Role, Number
from ..email import send_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:

        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


# 等待验证路由
@auth.route('/unconfirmed', methods=['GET', 'POST'])
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.commit'))
    return render_template('auth/unconfirmed.html')


# 登录路由
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                if user.role_id == 2:
                    next = url_for('main.welcome')
                else:
                    if current_user.enrolment:
                        next = url_for('main.information')
                    else:
                        next = url_for('main.commit')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


# 注册路由
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# 登出路由
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return render_template('index.html')


# 确认账户
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.commit'))


# 重新发送确认邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.commit'))


# 重置密码路由
@auth.route('/reset', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            flash('An email with instructions to reset your password has been '
                  'sent to you.')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


# 确认重置密码路由
@auth.route('/resrt/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.commit'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


# 修改密码路由
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已更改，请重新登录')
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


# 更改邮箱请求路由
@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.new_email.data
            token = current_user.generate_change_email_token(new_email)
            send_email(new_email, '确认邮件', 'auth/email/change_email',
                       user=current_user, token=token)
            flash('一个确认更换邮箱的邮件已发送到新邮箱中')
            return redirect(url_for('main.commit'))
        else:
            flash('请输入正确的邮箱和密码')
    return render_template('auth/change_email.html', form=form)


# 更改邮箱路由
@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('邮箱已更改，请重新登录')
        logout_user()
    else:
        flash('Invalid request')
    return redirect(url_for('auth.login'))