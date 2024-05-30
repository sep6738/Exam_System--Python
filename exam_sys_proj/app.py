from flask import Flask, session, g
import config
from exts import mail, db
from exam_sys_proj.private.models import Users
# from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# db.init_app(app)
mail.init_app(app)

# app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# blueprint：用来做模块化的


# before_request/ before_first_request/ after_request
# hook
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = Users.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}




if __name__ == '__main__':
    app.run()
