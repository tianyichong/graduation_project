from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    ValidationError, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class CommitForm(FlaskForm):
    submit = SubmitField('提交')


class EnrollForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    sex = StringField('性别', validators=[DataRequired()])
    id_number = StringField('身份证号', validators=[DataRequired()])
    nation = StringField('民族', validators=[DataRequired()])
    birthday = DateField('出生日期', validators=[DataRequired()])
    student_id = StringField('学籍号', validators=[DataRequired()])
    native_place = StringField('籍贯', validators=[DataRequired()])  # 籍贯
    political_status = StringField('政治面貌', validators=[DataRequired()])  # 政治面貌
    postal_address = StringField('通讯地址', validators=[DataRequired()])  # 通讯地址
    recipients = StringField('收件人', validators=[DataRequired()])  # 收件人
    contacts = StringField('联系人', validators=[DataRequired()])     # 联系人
    postal_code = StringField('邮政编码', validators=[DataRequired()])  # 邮编
    home_phone_number = StringField('宅电', validators=[DataRequired()])
    phone_number = StringField('手机号码', validators=[DataRequired()])
    high_school = StringField('毕业院校', validators=[DataRequired()])
    class_in_school = StringField('班级', validators=[DataRequired()])
    graduation_category = StringField('毕业类别', validators=[DataRequired()])  # 毕业类别
    examinee_category = StringField('考生类别', validators=[DataRequired()])  # 考生类别
    '''
    art_type = StringField('艺术统考类')  # 艺术统考类
    major = StringField('major')  # 专业方向
    sport = StringField('sport')  # 体育专业测试
    sport_project = StringField('sport_project')  # 体育测试项目
    '''
    headmaster = StringField('班主任', validators=[DataRequired()])  # 班主任
    speciality = StringField('特长', validators=[DataRequired()])  # 特长

    submit = SubmitField('提交')


class ChangeForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    sex = StringField('性别', validators=[DataRequired()])
    id_number = IntegerField('身份证号', validators=[DataRequired()])
    nation = StringField('民族', validators=[DataRequired()])
    birthday = DateField('出生日期', validators=[DataRequired()])
    student_id = IntegerField('学籍号', validators=[DataRequired()])
    native_place = StringField('籍贯', validators=[DataRequired()])  # 籍贯
    political_status = StringField('政治面貌', validators=[DataRequired()])  # 政治面貌
    postal_address = StringField('通讯地址', validators=[DataRequired()])  # 通讯地址
    recipients = StringField('收件人', validators=[DataRequired()])  # 收件人
    contacts = StringField('联系人', validators=[DataRequired()])     # 联系人
    postal_code = IntegerField('邮政编码', validators=[DataRequired()])  # 邮编
    home_phone_number = IntegerField('宅电', validators=[DataRequired()])
    phone_number = IntegerField('手机号码', validators=[DataRequired()])
    high_school = StringField('毕业院校', validators=[DataRequired()])
    class_in_school = StringField('班级', validators=[DataRequired()])
    graduation_category = StringField('毕业类别', validators=[DataRequired()])  # 毕业类别
    examinee_category = StringField('考生类别', validators=[DataRequired()])  # 考生类别
    '''
    art_type = StringField('艺术统考类')  # 艺术统考类
    major = StringField('major')  # 专业方向
    sport = StringField('sport')  # 体育专业测试
    sport_project = StringField('sport_project')  # 体育测试项目
    '''
    headmaster = StringField('班主任', validators=[DataRequired()])  # 班主任
    speciality = StringField('特长', validators=[DataRequired()])  # 特长

    submit = SubmitField('提交')


class SubmitForm(FlaskForm):
    submit = SubmitField('提交')


class InformationForm(FlaskForm):
    submit = SubmitField('修改')


class QueryInformationForm(FlaskForm):
    num = IntegerField('考生号', validators=[DataRequired()])
    submit = SubmitField('查询')


class QueryEssentialInformationForm(FlaskForm):
    num = IntegerField('考生号', validators=[DataRequired()])
    submit = SubmitField('查询')


class AddNumForm(FlaskForm):
    num = IntegerField('考生号', validators=[DataRequired()])
    sign_point = StringField('报名点', validators=[DataRequired()])
    exam_department = StringField('考试科类', validators=[DataRequired()])
    submit = SubmitField('添加')


class ChangeNumForm(FlaskForm):
    num = IntegerField('考生号', validators=[DataRequired()])
    sign_point = StringField('报名点', validators=[DataRequired()])
    exam_type = StringField('考试类型', validators=[DataRequired()])
    exam_department = StringField('考试科类', validators=[DataRequired()])
    submit = SubmitField('修改')


class DeleteNumForm(FlaskForm):
    num = IntegerField('考生号', validators=[DataRequired()])
    submit = SubmitField('删除')


class CheckForm(FlaskForm):
    pass
