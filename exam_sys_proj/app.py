import sys, os

# 添加搜索路径
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from exam_sys_proj.dao.UsersDAO import UsersDAO, Users
from flask import Flask, session, g, redirect, url_for
from exam_sys_proj.src import config
from exam_sys_proj.src.extensions import mail, dbPool
# from exam_sys_proj.private.models import Users
# from blueprints.qa import bp as qa_bp
from exam_sys_proj.blueprints.auth import bp as auth_bp
from exam_sys_proj.blueprints.teacher import bp as teacher_bp
from exam_sys_proj.blueprints.student import bp as student_bp
from exam_sys_proj.blueprints.admin import bp as admin_bp


# todo:导航条，创建实体，用户名显示，登出，未登录时跳转登陆界面

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
app.config['STATIC_URL'] = '/static'

users_operator = UsersDAO(dbPool)

# db.init_app(app)
mail.init_app(app)

app.register_blueprint(teacher_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)


# blueprint：用来做模块化的
# print(os.path.abspath('.'))
# print(os.getcwd())

# before_request/ before_first_request/ after_request
# hook
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user: Users = users_operator.query(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


@app.route('/')
def index():
    return redirect(url_for("auth.login"))


if __name__ == '__main__':
    app.run(host='127.0.1.3', port=5555)
