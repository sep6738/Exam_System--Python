from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from exam_sys_proj.src.extensions import mail, dbPool
from flask_mail import Message
from flask import request
from .forms import RegisterForm, LoginForm
import bcrypt
from exam_sys_proj.dao.RegistrationCodeDAO import RegistrationCodeDAO, RegistrationCode
from exam_sys_proj.dao.UsersDAO import UsersDAO, Users

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


# http://127.0.0.1:5000
@bp.route("/detail")
def detail():
    return render_template("teacher_detail.html")


@bp.route("/question_create")
def question_create():
    if request.method == 'GET':
        return render_template("teacher_question_create.html")
    # else:
    #     data = request.get_json()
    #     print(data)
    #     return jsonify({'message': 'Data received successfully'})


@bp.route("/api/question_create", methods=['POST'])
def question_create_api():
    data = request.get_json()
    print(data)
    return jsonify({'message': 'Data received successfully'})

# @bp.route("/qa/public", methods=['GET', 'POST'])
# @login_required
# def public_question():
#     if request.method == 'GET':
#         return render_template("public_question.html")
#     else:
#         form = QuestionForm(request.form)
#         if form.validate():
#             title = form.title.data
#             content = form.content.data
#             question = QuestionModel(title=title, content=content, author=g.user)
#             db.session.add(question)
#             db.session.commit()
#             # todo: 跳转到这篇问答的详情页
#             return redirect("/")
#         else:
#             print(form.errors)
#             return redirect(url_for("qa.public_question"))
#
#
# @bp.route("/qa/detail/<qa_id>")
# def qa_detail(qa_id):
#     question = QuestionModel.query.get(qa_id)
#     return render_template("detail.html", question=question)
#
#
# # @bp.route("/answer/public", methods=['POST'])
# @bp.post("/answer/public")
# @login_required
# def public_answer():
#     form = AnswerForm(request.form)
#     if form.validate():
#         content = form.content.data
#         question_id = form.question_id.data
#         answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
#         db.session.add(answer)
#         db.session.commit()
#         return redirect(url_for("qa.qa_detail", qa_id=question_id))
#     else:
#         print(form.errors)
#         return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))
#
#
# @bp.route("/search")
# def search():
#     # /search?q=flask
#     # /search/<q>
#     # post, request.form
#     q = request.args.get("q")
#     questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
#     return render_template("index.html", questions=questions)
