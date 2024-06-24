from flask import Blueprint, render_template, jsonify, redirect, url_for, session, flash, send_file
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
from ..dao.HepAndKpMediaterDAO import HepAndKpMediaterDAO
from ..dao.HomeworkOrExamPoolDAO import HomeworkOrExamPoolDAO
from ..dao.StudentCourseDAO import StudentCourseDAO
from ..dao.TeacherCourseDAO import TeacherCourseDAO
from ..util.HomeworkOrExamUtils import HomeworkOrExamUtils
from ..util.StudentHandinUtils import StudentHandinUtils
from ..util.studentcourseUtils import StudentCourseUtils
from ..util.teachercourseUtils import TeacherCourseUtils

bp = Blueprint("teacher", __name__, url_prefix="/teacher")


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        """
        判断是否为bytes类型的数据是的话转换成str
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


# http://127.0.0.1:5000
@bp.route("/detail")
def detail():
    broadcast_getter = BroadcastShowDAO(dbPool)
    broadcasts = broadcast_getter.get_user_All_Broadcast(session.get("user_id"))
    if broadcasts != 'noResult':
        for broadcast in broadcasts:
            broadcast.content = json.loads(broadcast.content)
            broadcast.content['message'] = Markup(
                markdown.markdown(broadcast.content['message'], extensions=['extra', 'codehilite', 'nl2br']))
    return render_template("teacher_detail.html", broadcasts=broadcasts)


@bp.route("/exam_manage")
def exam_manage():
    teacher_operator = TeacherCourseDAO(dbPool)
    courses = teacher_operator.query(session.get("user_id"), "userID", True)
    courses_data = []
    for course in courses:
        temp = {}
        temp['courseName'] = course.courseName
        exams = StudentHandinUtils.get_course_test(dbPool, course.courseID)
        temp['exams'] = json.loads(exams)
        courses_data.append(temp)

    data = {'courses': courses_data}
    return render_template("teacher_exam_manage.html", data=data)



@bp.route("/student_manage")
def student_manage():
    teacher_operator = TeacherCourseDAO(dbPool)
    courses = teacher_operator.query(session.get("user_id"), "userID", True)
    data = {'courses': courses}
    return render_template("teacher_student_manage.html", data=data)


@bp.route("/api/get_student/<courseID>")
def get_student_api(courseID):
    data = TeacherCourseUtils.getcourse_user(dbPool, courseID)
    for i in data:
        if i['createAt']:
            i['createAt'] = i['createAt'].strftime("%Y-%m-%d %H:%M:%S")
        if i['updateAt']:
            i['updateAt'] = i['updateAt'].strftime("%Y-%m-%d %H:%M:%S")
    # print(data)
    return json.dumps({
        'code': 0,
        'message': "成功！",
        'data': data
    }, cls=MyEncoder)


@bp.route("/api/add_student/<courseID>", methods=["POST"])
def add_student_api(courseID):
    data = request.get_json()
    # print(data)
    result = "请输入学生ID！"
    if data:
        for userID in data:
            result = StudentCourseUtils.insert_course_student(dbPool, courseID, userID)
    return json.dumps({
        'code': 0,
        'message': result,
        'data': result}, ensure_ascii=False)


@bp.route("/api/delete_student/<courseID>", methods=["POST"])
def delete_student_api(courseID):
    data = request.get_json()
    # print(data)
    result = "请选择学生！"
    if data:
        for userID in data:
            result = StudentCourseUtils.delete_course_student(dbPool, courseID, userID)
    return json.dumps({
        'code': 0,
        'message': result,
        'data': result}, ensure_ascii=False)


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
    file_received = request.files.get('file')
    filename = './' + str(session.get("user_id")) + '.json'
    file_received.save(filename)  # 在暂存的导入文件名前添加用户id，可以多个用户同时导入，导入后删除该文件
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
        question['answer'] = []
        question['main_content'] = data['main_content']
        question['type'] = '选择题'
        question['questions'] = [data['selection1'], data['selection2'], data['selection3'], data['selection4']]
        question['answer'].append(data['answer'])
        if data['analyze']:
            question['answer'].append(data['analyze'])
        else:
            question['answer'].append('')
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
        question['answer'] = []
        question['main_content'] = data['main_content']
        question['type'] = '判断题'
        question['questions'] = ["√", "X"]
        question['answer'].append(data['answer'])
        if data['analyze']:
            question['answer'].append(data['analyze'])
        else:
            question['answer'].append('')
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
    if not question['knowledge_point']:
        question['knowledge_point'].append('其它')
    print(question)
    TeacherUtils.insertOneQuestion(dbPool, question)
    return jsonify({'message': 'Data received successfully'})


@bp.route("/paper_create", methods=["GET", "POST"])
def paper_create():
    question_types = ['选择题', '判断题', '填空题', '主观题']
    knowledge_points = TeacherUtils.queryTeacherSubjectKP(dbPool, session.get("user_id"))
    if request.method == 'GET':
        if knowledge_points:
            return render_template("teacher_paper_create.html", question_types=question_types,
                                   knowledge_points=knowledge_points)
        else:
            return '您没有教授的课程，请联系管理员'
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
        paper['get_answer'] = True
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
    # print(paper)
    result = TeacherUtils.random_paper(paper, dbPool)
    print(result)
    if result['status_code'] == 404:
        return result['message']
    else:
        TeacherUtils.insertOneQuestion(dbPool, result['content'][1])
        return result['content'][2]


# @bp.route("/paper_publish", methods=["GET", "POST"])
# def paper_publish():
#     if request.method == 'GET':
#         papers_getter = HomeworkOrExamPoolDAO(dbPool)
#         subject = TeacherUtils.queryTeacherSubjectKP(dbPool, session.get("user_id"))
#         papers = papers_getter.query(subject, "courseName", True)
#         return render_template("teacher_paper_publish.html", papers=papers)


@bp.route("/question_manage")
def question_manage():
    teacher_operator = TeacherCourseDAO(dbPool)
    courses = teacher_operator.query(session.get("user_id"), "userID", True)
    subject = courses[0].subject
    chart_getter = HomeworkOrExamPoolDAO(dbPool)
    chart = chart_getter.get_type_analysis()
    #  截取图标html代码的body部分
    start_tag = "<body >"
    end_tag = "</body>"
    start_index = chart.find(start_tag)
    end_index = chart.find(end_tag) + len(end_tag)
    chart = chart[start_index:end_index]
    chart = chart.strip('<body >')
    chart = chart.strip('</body >')
    chart = Markup(chart)
    print(chart)
    return render_template("teacher_question_manage.html", subject=subject, chart=chart)


@bp.route("/api/get_question/<subject>")
def get_question_api(subject):
    question_operator = HomeworkOrExamPoolDAO(dbPool)
    data = question_operator.query(subject, "courseName", True)
    questions = []
    if data:
        for i in data:
            singe_question = {}
            singe_question['hepID'] = i.hepID
            singe_question['type'] = i.type
            question = json.loads(i.question)
            singe_question['score'] = question['score']
            singe_question['shuffle'] = question['shuffle']
            singe_question['questions'] = question['questions']
            singe_question['main_content'] = question['main_content']
            singe_question['subject'] = i.courseName
            singe_question['difficulty'] = i.difficultyLevel
            questions.append(singe_question)
    return json.dumps({
        'code': 0,
        'message': "成功！",
        'data': questions
    }, cls=MyEncoder)


@bp.route("/paper_publish", methods=["GET", "POST"])
def paper_publish():
    if request.method == 'GET':
        getter = HomeworkOrExamPoolDAO(dbPool)
        data = getter.query('考试', "type", True)
        papers = []
        if data:
            for i in data:
                paper = {
                    'hepID': i.hepID,
                    'title': json.loads(i.question)['main_content']
                }
                papers.append(paper)

        teacher_operator = TeacherCourseDAO(dbPool)
        courses = teacher_operator.query(session.get("user_id"), "userID", True)

        return render_template("teacher_paper_publish.html", papers=papers, courses=courses)
    else:
        examID = request.form.get("examID")
        courseID = request.form.get("courseID")
        publishTime = request.form.get("publishTime")
        deadline = request.form.get("deadline")
        duration = request.form.get("duration")
        result = HomeworkOrExamUtils.insert_homeworkOrexam(dbPool, examID, courseID, publishTime, deadline, duration)
        if result:
            flash("试卷发布成功！")
        else:
            flash("试卷发布失败，请重试！")

        return redirect(url_for("teacher.paper_publish"))


@bp.route("/api/delete_question/<hepID>")
def delete_question_api(hepID):
    question_operator = HomeworkOrExamPoolDAO(dbPool)
    knowledge_point_mediator_operator = HepAndKpMediaterDAO(dbPool)
    r1 = question_operator.delete(hepID)
    r2 = knowledge_point_mediator_operator.delete(hepID, "hepID")

    if r1 and r2:

        return jsonify({
            'code': 0,
            'message': "成功！",
            'data': {}})
    else:
        return jsonify({
            'code': 1,
            'message': "失败！",
            'data': {}
        })


@bp.route("/api/get_question_detail/<hepID>", methods=["GET"])
def get_question_detail(hepID):
    question_operator = HomeworkOrExamPoolDAO(dbPool)
    question = question_operator.query(hepID)
    if question:
        question_dict = {
            "hepID": question.hepID,
            "type": question.type,
            "question": json.loads(question.question),
            "answer": json.loads(question.answer),
            "courseName": question.courseName,
            "difficultyLevel": question.difficultyLevel,
            "isActive": bool(question.isActive),
        }
        return json.dumps({
            "code": 0,
            "message": "成功",
            "data": question_dict
        })
    else:
        return json.dumps({
            "code": 1,
            "message": "试题不存在",
            "data": {}
        })


@bp.route("/export")
def export():
    getter = HomeworkOrExamPoolDAO(dbPool)
    data = getter.query('考试', "type", True)
    # data = getter.queryAll(count=0)
    papers = []
    paper = {}
    # print(data)
    if data:
        for i in data:
            # print(i)
            # print(i.type)
            # if i.type in ['考试', '测试', '作业', '其它']:
            paper['hepID'] = i.hepID
            paper['title'] = json.loads(i.question)['main_content']
            papers.append(paper)
    subject_getter = TeacherCourseDAO(dbPool)
    subjects = subject_getter.getallsubject()
    return render_template("teacher_export.html", papers=papers, subjects=subjects)


@bp.route('/download_questions', methods=['POST'])
def download_questions():
    path = 'temp\\' + request.form['subject'] + '.json'
    if TeacherUtils.export_questions(dbPool, request.form['subject'], 'exam_sys_proj\\' + path):
        return {'redirect_url': f'/teacher/download/' + request.form['subject'] + '.json'}
        # return send_file(path, as_attachment=True)


@bp.route("/download/<path>")
def download(path):
    return send_file('temp\\' + path, as_attachment=True)


@bp.route('/download_paper', methods=['POST'])
def download_paper():
    path = 'temp\\' + request.form['hepID'] + '.docx'
    TeacherUtils.export_paper_as_docx(dbPool, int(request.form['hepID']), 'exam_sys_proj\\' + path)
    return {'redirect_url': f'/teacher/download/' + request.form['hepID'] + '.docx'}
