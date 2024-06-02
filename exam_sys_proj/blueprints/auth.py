from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from exam_sys_proj.src.extensions import mail, dbPool
from flask_mail import Message
from flask import request
from .forms import RegisterForm, LoginForm
import bcrypt
from exam_sys_proj.dao.RegistrationCodeDAO import RegistrationCodeDAO, RegistrationCode
from exam_sys_proj.dao.UsersDAO import UsersDAO, Users

# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")
users_operator = UsersDAO(dbPool)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user: Users = users_operator.query(email, 'email')
            # user = Users.query.filter_by(email=email).first()
            if not user:
                print("邮箱未注册！")
                return redirect(url_for("auth.login"))
            if bcrypt.checkpw(password.encode("utf-8"), user.passWord):
                # cookie：
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.userID
                if user.roleID == 1:
                    return redirect("/student/detail")
                if user.roleID == 2:
                    return redirect("/teacher/detail")
            else:
                flash(f"密码错误！", 'danger')
                return redirect(url_for("auth.login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    # flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                    flash(f"{error}", 'danger')
            return redirect(url_for("auth.login"))


# GET：从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：src-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            name = form.name.data
            user = Users(userName=username, passWord=password, name=name, roleID=1, email=email)
            users_operator.insert(user)
            # user = Users(email=email, username=username, password=generate_password_hash(password))
            # db.session.add(user)
            # db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    # flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
                    flash(f"{error}", 'danger')
            return redirect(url_for("auth.register"))
            # return render_template('register.html', form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/auth/login")


# bp.route：如果没有指定methods参数，默认就是GET请求
@bp.route("/captcha/email")
def get_email_captcha():
    register = RegistrationCodeDAO(dbPool)

    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    # 4/6：随机数组、字母、数组和字母的组合
    # src = (string.digits+string.ascii_uppercase)*6
    # captcha = random.sample(src, 6)
    # captcha = "".join(captcha)
    # I/O：Input/Output
    registerOrm = RegistrationCode()
    message = Message(subject="好得不能再好了！测试系统验证码", recipients=[email],
                      body=f"恭喜您受邀参与“好得不能再好了测试系统”的内测，您的验证码是:{registerOrm.verificationCode}，测试网址请向坎诺特先生支付1000至纯源石获得")
    mail.send(message)
    # memcached/redis
    # 用数据库表的方式存储
    register.SetVerificationCode(registerOrm, email)
    # email_captcha = RegistrationCode(email=email,verificationCode=captcha,expirationDate=datetime.datetime.now()+datetime.timedelta(minutes=5))
    # db.session.add(email_captcha)
    # db.session.commit()
    # RESTful API
    # {code: 200/400/500, message: "", data: {}}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["2063331724@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功！"
