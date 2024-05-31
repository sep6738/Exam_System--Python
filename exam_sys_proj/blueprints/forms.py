import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
# from models import Users, RegistrationCode
from exts import dbPool
from exam_sys_proj.dao.RegistrationCodeDAO import RegistrationCodeDAO, RegistrationCode
from exam_sys_proj.dao.UsersDAO import UsersDAO, Users
from datetime import datetime

# Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=1, max=20, message="用户名格式错误！")])
    name = wtforms.StringField(validators=[Length(min=1, max=20, message="姓名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=9, max=20, message="密码长度需在9到20位之间！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证：
    # 1. 邮箱是否已经被注册
    def validate_email(self, field):
        email = field.data
        usersOperator = UsersDAO(dbPool)
        user = usersOperator.query(email)
        # user = Users.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data.upper()
        email = self.email.data
        varificater = RegistrationCodeDAO(dbPool)
        entity : RegistrationCode = varificater.query(email)
        if captcha != entity.verificationCode or entity.expirationDate < datetime.now():
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        # captcha_model = RegistrationCode.query.filter_by(email=email, captcha=captcha).first()
        # if not captcha_model:
        #     raise wtforms.ValidationError(message="邮箱或验证码错误！")
        # else:)
        #     #
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

# class QuestionForm(wtforms.Form):
#     title = wtforms.StringField(validators=[Length(min=3, max=100, message="标题格式错误！")])
#     content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误！")])
#
#
# class AnswerForm(wtforms.Form):
#     content = wtforms.StringField(validators=[Length(min=3, message="内容格式错误！")])
#     question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题id！")])
