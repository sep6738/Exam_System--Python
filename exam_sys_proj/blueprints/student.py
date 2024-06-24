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
from ..dao.HepAndKpMediaterDAO import HepAndKpMediaterDAO
from ..dao.HomeworkOrExamPoolDAO import HomeworkOrExamPoolDAO
from ..dao.KnowledgePointsDAO import KnowledgePointsDAO
from ..dao.StudentCourseDAO import StudentCourseDAO
from ..dao.StudentHandInDAO import StudentHandInDAO
from ..dao.TeacherCourseDAO import TeacherCourseDAO
from ..orm.StudentHandIn import StudentHandIn
from ..util.StudentHandinUtils import StudentHandinUtils

# from ..dao.studentCourseDAO import studentCourseDAO

bp = Blueprint("student", __name__, url_prefix="/student")


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
    return render_template("student_detail.html", broadcasts=broadcasts)


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


@bp.route("/paper_create/<subject>", methods=["GET", "POST"])
def paper_create(subject):
    question_types = ['选择题', '判断题', '填空题', '主观题']
    knowledge_point_getter = KnowledgePointsDAO(dbPool)
    knowledge_points = knowledge_point_getter.query(subject, 'subject', True)
    if request.method == 'GET':
        return render_template("student_paper_create.html", question_types=question_types,
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
        paper['get_answer'] = False
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
    # TODO:传入Content
    print(paper)
    return 'Data received successfully'


@bp.route('/select_subject', methods=['POST', 'GET'])
def select_subject():
    if request.method == 'POST':
        subject = request.form['subject']
        # 将学科参数传递到新页面
        return {'redirect_url': f'/student/paper_create/{subject}'}
    else:
        subject_getter = TeacherCourseDAO(dbPool)
        subjects = subject_getter.getallsubject()
        if subjects:
            return render_template('student_select_subject.html', subjects=subjects)
        else:
            return "没有学科！"


@bp.route('/exam_list')
def exam_list():
    return render_template('student_exam.html')


@bp.route('/get_papers')
def get_papers():
    student_id = session.get("user_id")
    # papers: list[StudentHandIn] = student_hand_in_dao.query(student_id, 'userID', True)
    papers = StudentHandinUtils.get_user_test(dbPool, student_id)
    # print(papers)
    # paper_details = []
    # for paper in papers:
    #     paper_detail = {
    #         'paperID': paper.studentHandInID,
    #         'title': paper.content,
    #         'subject': paper,
    #         'score': paper.score
    #         # 'completed': paper.completed
    #     }
    #     paper_details.append(paper_detail)
    return json.dumps({
        'code': 0,
        'message': "成功！",
        'data': json.loads(papers)
    }, cls=MyEncoder)
    # return jsonify({'code': 0, 'data': papers})


# @bp.route('/view_paper', methods=['POST'])
# def view_paper():
#     data = request.get_json()
#     studentHandInID = data.get('studentHandInID')
#     return jsonify({'redirect_url': 'student.view_paper/'+studentHandInID})

@bp.route('/view_paper/{paper_id}', methods=['GET'])
def view_paper_detail(paper_id):
    teacherUtils = TeacherUtils()
    teacherUtils.getPaperForShow(paper_id, dbPool)


@bp.route('/start_exam/<paper_id>')
def start_exam(paper_id):
    teacherUtils = TeacherUtils()
    paper = teacherUtils.getPaperForShow(int(paper_id), dbPool)
    paper = json.dumps(paper, ensure_ascii=False)
    print(paper)
    return render_template('exam_answer.html', paper=paper, paper_id=paper_id)


@bp.route('/submit_answers', methods=['POST'])
def submit_exam():
    answers = request.get_json()
    print(answers)
    answers = answers['answers']
    # 处理答案，保存到数据库或其他逻辑
    # 示例：将答案打印到控制台
    paper_id = int(answers.pop())
    data = []
    for i in answers:
        temp = []
        if type(i) == int:
            i = str(i)
        temp.append(i)
        data.append(temp)
    print(f"HandIn ID: {paper_id}, Answers: {data}")
    studentHandInDAO = StudentHandInDAO(dbPool)
    data = json.dumps(data)
    entity = StudentHandIn(studentHandInID=paper_id, content=data)
    studentHandInDAO.update(entity, paper_id)
    StudentHandinUtils.auto_correct(dbPool, paper_id)
    return jsonify({'message': '答案提交成功！'})
