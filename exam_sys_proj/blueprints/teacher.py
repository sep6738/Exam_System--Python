from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from exam_sys_proj.src.extensions import mail, dbPool
from flask_mail import Message
from flask import request
from .forms import RegisterForm, LoginForm
import bcrypt
from exam_sys_proj.dao.RegistrationCodeDAO import RegistrationCodeDAO, RegistrationCode
from exam_sys_proj.dao.UsersDAO import UsersDAO, Users
from exam_sys_proj.util.teacherUtils import TeacherUtils

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


# http://127.0.0.1:5000
@bp.route("/detail")
def detail():
    return render_template("teacher_detail.html")


@bp.route("/question_import")
def question_import():
    return render_template("teacher_question_import.html")


@bp.route("/api/question_import", methods=['GET', 'POST'])
def question_import_api():
    print('文件接受成功')
    fileRecived = request.files.get('file')
    fileRecived.save('./import.json')
    with open('./import.json', 'r') as f:
        print(f.read())
    return jsonify({
        'code': 0,
        'message': "成功！",
        'data': {
        }
    })


@bp.route("/question_create")
def question_create():
    if request.method == 'GET':
        knowledge_points = TeacherUtils.queryTeacherSubjectKP(dbPool, session.get("user_id"))
        # print(knowledge_points)
        return render_template("teacher_question_create.html", knowledge_points=knowledge_points)
    # else:
    #     data = request.get_json()
    #     print(data)
    #     return jsonify({'message': 'Data received successfully'})


@bp.route("/api/question_create", methods=['POST'])
def question_create_api():
    data = request.get_json()
    # print(data)
    question = {}
    if data['question_type'] == '选择题':
        question['main_content'] = data['main_content']
        question['type'] = '选择题'
        question['questions'] = [data['selection1'], data['selection2'], data['selection3'], data['selection4']]
        question['answer'] = []
        question['answer'].append(data['answer'])
        if 'shuffle' in data:
            question['shuffle'] = True
        else:
            question['shuffle'] = False
        question['subject'] = data['subject']
        question['difficulty'] = int(data['difficulty'])
        question['score'] = []
        question['score'].append(float(data['score']))
        question['knowledge_point'] = []
        for i in data.keys():
            if i.startswith('knowledge_point'):
                question['knowledge_point'].append(i[16:])
    elif data['question_type'] == '判断题':
        question['main_content'] = data['main_content']
        question['type'] = '判断题'
        question['questions'] = ["√", "X"]
        question['answer'] = []
        question['answer'].append(data['answer'])
        question['shuffle'] = True
        question['subject'] = data['subject']
        question['difficulty'] = int(data['difficulty'])
        question['score'] = []
        question['score'].append(float(data['score']))
        question['knowledge_point'] = []
        for i in data.keys():
            if i.startswith('knowledge_point'):
                question['knowledge_point'].append(i[16:])
    elif data['question_type'] == '填空题':
        question['main_content'] = data['main_content']
        question['type'] = '填空题'
        question['questions'] = []
        question['questions'].append(None)
        question['answer'] = []
        question['answer'].append(data['answer'])
        question['shuffle'] = False
        question['subject'] = data['subject']
        question['difficulty'] = int(data['difficulty'])
        question['score'] = []
        question['score'].append(float(data['score']))
        question['knowledge_point'] = []
        for i in data.keys():
            if i.startswith('knowledge_point'):
                question['knowledge_point'].append(i[16:])
    elif data['question_type'] == '主观题':
        question['main_content'] = data['main_content']
        question['type'] = '选择题'
        question['questions'] = []
        question['answer'] = []
        question['score'] = []
        question['knowledge_point'] = []
        for key, value in data.items():
            if key.startswith('knowledge_point'):
                question['knowledge_point'].append(key[16:])
            elif key.startswith('answer'):
                question['answer'].append(value)
            elif key.startswith('score'):
                question['score'].append(float(value))
            elif key.startswith('childQuestion'):
                question['questions'].append(value)
            question['shuffle'] = False
        question['subject'] = data['subject']
        question['difficulty'] = int(data['difficulty'])

    print(question)
    TeacherUtils.insertOneQuestion(dbPool, question)
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
