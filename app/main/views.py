from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import main
from .forms import CommitForm, EnrollForm, InformationForm, SubmitForm, ChangeForm, \
    QueryInformationForm, QueryEssentialInformationForm, AddNumForm, DeleteNumForm, ChangeNumForm, CheckForm
from .. import db, login_manager
from ..models import User, Number, Role
from ..decorators import admin_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/admin/<username>', methods=['GET', 'POST'])
def admin(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('admin.html', user=user)


@main.route('/instruction_candidates', methods=['GET', 'POST'])
def instruction_candidates():
    return render_template('instruction_candidates.html')


@main.route('/register_process', methods=['GET', 'POST'])
def register_process():
    return render_template('register_process.html')


@main.route('/pay_process', methods=['GET', 'POST'])
def pay_process():
    return render_template('pay_process.html')


@main.route('/commit', methods=['GET', 'POST'])
def commit():
    form = CommitForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            current_user.commitment = True
            db.session.commit()
            return redirect(url_for('main.enroll'))
    return render_template('commit.html', form=form)


@main.route('/enroll', methods=['GET', 'POST'])
def enroll():
    form = EnrollForm()
    if form.validate_on_submit():
        current_user.enrolment = True

        current_user.name = form.name.data
        current_user.sex = form.sex.data
        current_user.id_number = form.id_number.data

        current_user.nation = form.nation.data
        current_user.birthday = form.birthday.data
        current_user.student_id = form.student_id.data
        current_user.native_place = form.native_place.data
        current_user.political_status = form.political_status.data
        current_user.postal_address = form.postal_address.data
        current_user.recipients = form.recipients.data
        current_user.contacts = form.contacts.data
        current_user.postal_code = form.postal_code.data
        current_user.home_phone_number = form.home_phone_number.data
        current_user.phone_number = form.phone_number.data
        current_user.high_school = form.high_school.data
        current_user.class_in_school = form.class_in_school.data
        current_user.graduation_category = form.graduation_category.data
        current_user.examinee_category = form.examinee_category.data
        current_user.headmaster = form.headmaster.data
        current_user.speciality = form.speciality.data

        db.session.commit()
        return redirect(url_for('main.information'))
    return render_template('enroll.html', form=form)


@main.route('/information', methods=['GET', 'POST'])
def information():
    form = InformationForm()
    if form.validate_on_submit():
        return redirect(url_for('main.change'))
    return render_template('information.html', form=form)


@main.route('/change_information', methods=['GET', 'POST'])
def change():
    form = ChangeForm()

    if form.validate_on_submit():
        current_user.repeat += 1
        current_user.name = form.name.data
        current_user.sex = form.sex.data
        current_user.id_number = form.id_number.data

        current_user.nation = form.nation.data
        current_user.birthday = form.birthday.data
        current_user.student_id = form.student_id.data
        current_user.native_place = form.native_place.data
        current_user.political_status = form.political_status.data
        current_user.postal_address = form.postal_address.data
        current_user.recipients = form.recipients.data
        current_user.contacts = form.contacts.data
        current_user.postal_code = form.postal_code.data
        current_user.home_phone_number = form.home_phone_number.data
        current_user.phone_number = form.phone_number.data
        current_user.high_school = form.high_school.data
        current_user.class_in_school = form.class_in_school.data
        current_user.graduation_category = form.graduation_category.data
        current_user.examinee_category = form.examinee_category.data
        current_user.headmaster = form.headmaster.data
        current_user.speciality = form.speciality.data
        db.session.commit()
        return redirect(url_for('main.information'))
    form.name.data = current_user.name
    form.sex.data = current_user.sex
    form.id_number.data = current_user.id_number

    form.nation.data = current_user.nation
    form.birthday.data = current_user.birthday
    form.student_id.data = current_user.student_id
    form.native_place.data = current_user.native_place
    form.political_status.data = current_user.political_status
    form.postal_address.data = current_user.postal_address
    form.recipients.data = current_user.recipients
    form.contacts.data = current_user.contacts
    form.postal_code.data = current_user.postal_code
    form.home_phone_number.data = current_user.home_phone_number
    form.phone_number.data = current_user.phone_number
    form.high_school.data = current_user.high_school
    form.class_in_school.data = current_user.class_in_school
    form.graduation_category.data = current_user.graduation_category
    form.examinee_category.data = current_user.examinee_category
    form.headmaster.data = current_user.headmaster
    form.speciality.data = current_user.speciality
    return render_template('change_information.html', form=form)


@main.route('/welcome')
def welcome():
    return render_template('welcome.html')


@admin_required
@main.route('/check', methods=['GET', 'POST'])
def check():
    form = CheckForm()
    users = User.query.filter_by(enrolment=True).all()
    sum = len(users)
    return render_template('check.html', form=form, users=users, sum=sum)


# 查询详细信息
@admin_required
@main.route('/query_information', methods=['GET', 'POST'])
def query_information():
    form = QueryInformationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(number=form.num.data).first()
        if user:
            if user.name:
                return render_template('query_information.html', form=form, user=user)
            else:
                flash('该学生还未报名')
        else:
            flash('不存在该学生')
    return render_template('query_information.html', form=form)


# 查询基本信息
@admin_required
@main.route('/query_essential_information', methods=['GET', 'POST'])
def query_essential_information():
    form = QueryEssentialInformationForm()
    if form.validate_on_submit():
        number = Number.query.filter_by(num=form.num.data).first()
        if number:
            return render_template('query_essential_information.html', form=form, number=number)
        else:
            flash('该考生号的基本信息不存在')
    return render_template('query_essential_information.html', form=form)


@admin_required
@main.route('/add_num', methods=['GET', 'POST'])
def add_num():
    form = AddNumForm()

    if form.validate_on_submit():
        number = Number()
        number.num = form.num.data
        number.sign_point = form.sign_point.data
        number.exam_department = form.exam_department.data
        if Number.query.filter_by(num=form.num.data).first():
            flash('该考生号的基本信息已存在')
        else:
            db.session.add(number)
            db.session.commit()
            return render_template('add_num.html', form=form, number=number)
    return render_template('add_num.html', form=form)


@admin_required
@main.route('/delete_num', methods=['GET', 'POST'])
def delete_num():
    form = DeleteNumForm()
    if form.validate_on_submit():
        number = Number.query.filter_by(num=form.num.data).first()
        if number:
            db.session.delete(number)
            db.session.commit()
            flash('该考生号的基本信息已删除')
        else:
            flash('该考生号不出在')
    return render_template('delete_num.html', form=form)


@admin_required
@main.route('/change_num', methods=['GET', 'POST'])
def change_num():
    form = ChangeNumForm()
    if form.validate_on_submit():
        number = Number.query.filter_by(num=form.num.data).first()
        if number.num:
            number.sign_point = form.sign_point.data
            number.exam_type = form.exam_type.data
            number.exam_department = form.exam_department.data
            return render_template('change_num.html', form=form, number=number)
        else:
            flash('该考生号的基本信息不存在')
    return render_template('change_num.html', form=form)
