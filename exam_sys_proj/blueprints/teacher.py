from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash
from exam_sys_proj.src.extensions import mail, dbPool
from flask_mail import Message
from flask import request
from .forms import RegisterForm, LoginForm
import os, bcrypt, json, markdown
from markupsafe import Markup
from exam_sys_proj.dao.RegistrationCodeDAO import RegistrationCodeDAO, RegistrationCode
from exam_sys_proj.dao.UsersDAO import UsersDAO, Users
from exam_sys_proj.util.teacherUtils import TeacherUtils
from exam_sys_proj.dao.BroadcastShowDAO import BroadcastShowDAO

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


# http://127.0.0.1:5000
@bp.route("/detail")
def detail():
    broadcast_getter = BroadcastShowDAO(dbPool)
    broadcasts = broadcast_getter.get_user_All_Broadcast(session.get("user_id"))
    for broadcast in broadcasts:
        broadcast.content = json.loads(broadcast.content)
        broadcast.content['message'] = Markup(
            markdown.markdown(broadcast.content['message'], extensions=['extra', 'codehilite', 'nl2br']))
    return render_template("teacher_detail.html", broadcasts=broadcasts)


@bp.route("/change_password", methods=["POST"])
def change_password():
    data = request.get_json()
    user_id = session.get("user_id")
    users_operator = UsersDAO(dbPool)
    user: Users = users_operator.query(user_id)
    if len(data['new_password']) < 9 or len(data['new_password']) > 20:
        return '密码长度需在9到20位之间！'
    elif bcrypt.checkpw(data['old_password'].encode("utf-8"), user.passWord):
        newpassword = Users(passWord=data['new_password'])
        users_operator.update(newpassword, user.userID)
        return '修改成功！'
    else:
        return '密码错误！'

@bp.route("/question_import")
def question_import():
    return render_template("teacher_question_import.html")


@bp.route("/api/question_import", methods=['GET', 'POST'])
def question_import_api():
    print('文件接受成功')
    file_recived = request.files.get('file')
    filename = './' + str(session.get("user_id")) + '.json'
    file_recived.save(filename)  # 在暂存的导入文件名前添加用户id，可以多个用户同时导入，导入后删除该文件
    TeacherUtils.batchInsertQuestions(dbPool, filename)
    # with open(filename, 'r',encoding='utf-8') as f:
    # print(f.read())
    os.remove(filename)
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
        question['type'] = '主观题'
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


@bp.route("/paper_create", methods=["GET", "POST"])
def paper_create():
    question_types = ['选择题', '判断题', '填空题', '主观题']
    knowledge_points = TeacherUtils.queryTeacherSubjectKP(dbPool, session.get("user_id"))
    if request.method == 'GET':
        return render_template("teacher_paper_create.html", question_types=question_types,
                               knowledge_points=knowledge_points)
    else:
        data = request.get_json()
        # print(data)
        paper = {}
        paper['title'] = data['title']
        paper['subject'] = data['subject']
        paper['type'] = data['type']
        paper['overall_difficulty_easy'] = data['overall_difficulty_easy']
        paper['overall_difficulty_normal'] = data['overall_difficulty_normal']
        paper['overall_difficulty_hard'] = data['overall_difficulty_hard']
        if 'shuffle' in data:
            paper['shuffle'] = False
        else:
            paper['shuffle'] = True
        for question_type in question_types:
            paper[question_type] = {}
            if question_type != "主观题":
                paper[question_type]["score_per_question"] = data[question_type + "_score_per_question"]
            else:
                paper[question_type]["score_per_question"] = '0'
            paper[question_type]["difficulty_min"] = data[question_type + "_difficulty_min"]
            paper[question_type]["difficulty_max"] = data[question_type + "_difficulty_max"]
            paper[question_type]["amount_per_knowledge_point"] = {}
            for knowledge_point in knowledge_points:
                paper[question_type]["amount_per_knowledge_point"][knowledge_point.kpName] = data[
                    question_type + "_" + knowledge_point.kpName]
    print(paper)
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
