import json
from datetime import datetime
from pyecharts.charts import Line
from exam_sys_proj.dao.HomeworkOrExamPoolDAO import HomeworkOrExamPoolDAO
from exam_sys_proj.dao.StudentHandInDAO import StudentHandInDAO
from exam_sys_proj.orm.HomeworkOrExamPool import HomeworkOrExamPool
from exam_sys_proj.orm.StudentHandIn import StudentHandIn
from exam_sys_proj.util.teacherUtils import TeacherUtils
from pyecharts.options import TitleOpts, LegendOpts, ToolboxOpts, AxisOpts

class StudentHandinUtils:
    @classmethod
    def auto_correct(cls, db_util, studenthandinId: int):
        try:
            query = f"SELECT hep.type,hep.question,hep.answer FROM student_hand_in shi,homework_or_exam hp,homework_or_exam_pool hep WHERE shi.homeworkExamID=hp.heID and hp.homeworkExamPoolID=hep.hepID and shi.studenthandinID=%s"
            conn = db_util.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (studenthandinId,))
                    ans = cursor.fetchall()
            finally:
                conn.close()
            dao = StudentHandInDAO(db_util)
            result = dao.query(studenthandinId)
            entity_class = StudentHandIn()
            columns = [attr for attr in dir(entity_class) if
                       not callable(getattr(entity_class, attr)) and not attr.startswith("_")]
            data = {}
            for attr in columns:
                data[attr] = getattr(result, attr)

            content = json.loads(data['content'])
            # 提交的答案
            answer = json.loads(ans[0][2])
            # 正确答案
            questions = json.loads(ans[0][1])['questions']
            scores = json.loads(ans[0][1])['score']
            # setattr(result, 'testPaper', json.dumps(ans[0][1], ensure_ascii=False))
            total =0
            # return None
            pos = 0
            idea = 0
            details = {}
            if '选择题' in questions.keys():
                cnt = len(questions['选择题']) - 1
                score = 0
                correct = 0
                for i in range(pos, pos + cnt):
                    if content[i][0] == answer[i][0]:
                        score = score + scores[idea][i - pos]
                        correct += 1
                    total += scores[idea][i-pos]
                details['选择题得分'] = score
                details['选择题回答正确个数'] = correct
                details['选择题总个数'] = cnt
                pos = pos+cnt
                idea = idea + 1
            if '判断题' in questions.keys():
                cnt = len(questions['判断题']) - 1
                score = 0
                correct = 0
                for i in range(pos, pos + cnt):
                    if content[i][0] == answer[i][0]:
                        score = score + scores[idea][i-pos]
                        correct += 1
                    total += scores[idea][i-pos]
                details['判断题得分'] = score
                details['判断题回答正确个数'] = correct
                details['判断题总个数'] = cnt
            details['试卷满分'] = total
            # print(details)
            setattr(result, 'resultDetails', json.dumps(details, ensure_ascii=False))
            dao.update(result, studenthandinId)
            return '选择题和判断题批改成功'
        except Exception as e:
            print(e)
            return 'error'

    # 以下为自测试卷
    @classmethod
    def insert_self_exam(cls, db_util, test: list, userid: int):
        '''
        传入试卷的内容和答案，以及用户id，往student_hand_in表里面创建试卷，返回主键值
        :param test:
        :param db_util:
        :param test_paper:
        :param answer_list:
        :param userid:
        :return:
        '''
        try:
            # test_paper = json.loads(test[0])
            test_paper = test[0]
            answer_list = test[3]
            test_paper['answer'] = answer_list
            dao = StudentHandInDAO(db_util)
            entity = StudentHandIn()
            setattr(entity, 'userID', userid)
            setattr(entity, 'testPaper', json.dumps(test_paper))
            setattr(entity, 'homeworkExamID', -1)
            setattr(entity, 'createTime', datetime.now())
            pri = dao.insert(entity, 0)
            return pri
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def get_user_content(cls, db_util, content: list, studenthandinId: int):
        try:
            dao = StudentHandInDAO(db_util)
            result = dao.query(studenthandinId)
            setattr(result, 'upTime', datetime.now())
            setattr(result, 'content', json.dumps(content, ensure_ascii=False))
            test_paper = getattr(result, 'testPaper')
            answer = json.loads(test_paper)['answer']
            questions = json.loads(test_paper)['questions']
            scores = json.loads(test_paper)['score']

            pos = 0
            idea = 0
            details = {}
            if '选择题' in questions.keys():
                cnt = len(questions['选择题']) - 1
                score = 0
                correct = 0
                for i in range(pos, pos + cnt):
                    if content[i][0] == answer[i][0]:
                        score = score + scores[idea][i - pos]
                        correct += 1
                details['选择题得分'] = score
                details['选择题回答正确个数'] = correct
                details['选择题总个数'] = cnt
                pos = pos + cnt
                idea = idea + 1
            if '判断题' in questions.keys():
                cnt = len(questions['判断题']) - 1
                score = 0
                correct = 0
                for i in range(pos, pos + cnt):
                    if content[i][0] == answer[i][0]:
                        score = score + scores[idea][i-pos]
                        correct += 1
                details['判断题得分'] = score
                details['判断题回答正确个数'] = correct
                details['判断题总个数'] = cnt
            setattr(result, 'resultDetails', json.dumps(details, ensure_ascii=False))
            dao.update(result, studenthandinId)
            return '选择题和判断题批改成功'
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def get_user_test(cls, db_util, userID: int):
        '''
        试卷返回title,score,type,paperID,subject,homeworkOrExamID,studentHandInID
        自测返回title,score,type,paperID=-1,subject=None,paper,homeworkOrExamID=-1,studentHandInID
        :param db_util:
        :param userID:
        :return:
        '''
        try:
            query = f"SELECT hp.homeworkExamPoolID,hep.question,hep.courseName,shi.score,hep.type,hp.heID,shi.studentHandInID FROM student_hand_in shi,homework_or_exam hp,homework_or_exam_pool hep WHERE shi.homeworkExamID=hp.heID and hp.homeworkExamPoolID=hep.hepID and shi.userID=%s and shi.homeworkExamID != -1"
            conn = db_util.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (userID,))
                    resultset = cursor.fetchall()
            finally:
                conn.close()
            result = []
            for item in resultset:
                dic = dict()
                dic['paperID'] = item[0]
                question = json.loads(item[1])
                dic['title'] = question['main_content']
                dic['subject'] = item[2]
                dic['score'] = item[3]
                dic['type'] = item[4]
                dic['homeworkOrExamID'] = item[5]
                dic['studentHandInID'] = item[6]
                result.append(dic)
            studenthandindao = StudentHandInDAO(db_util)
            query_list = studenthandindao.query(-1, 'homeworkExamID', '1')

            if query_list is not None:
                for item in query_list:
                    dic = dict()
                    dic['type'] = '自测'
                    question = json.loads(getattr(item, 'testPaper'))
                    dic['title'] = question['main_content']
                    dic['score'] = getattr(item, 'score')
                    dic['paper'] = json.dumps(question, ensure_ascii=False)
                    dic['paperID'] = -1
                    dic['subject'] = None
                    dic['studentHandInID'] = item.studentHandInID
                    dic['homeworkOrExamID'] = -1
                    result.append(dic)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def get_course_test(cls, db_util, courseID: int):
        '''
        班级发布所有试卷的情况，返回userID,studentHandInID,score(控制返回None),content(0/1),userName
        {'userID': 778, 'studentHandInID': 2, 'score': 93.0, 'content': 1, 'userName': '兰斯洛特·杜·拉克'}
        :param db_util:
        :param courseID:
        :return:
        '''
        try:
            query = f"SELECT shi.userID,shi.studentHandInID,shi.score,shi.content,user.userName FROM student_hand_in shi,homework_or_exam hp,users user WHERE shi.homeworkExamID=hp.heID and hp.courseID=%s and user.userID = shi.userID"
            conn = db_util.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (courseID,))
                    resultset = cursor.fetchall()
            finally:
                conn.close()
            result = []
            if resultset is not None:
                for item in resultset:
                    dic = dict()
                    dic['userID'] = item[0]
                    dic['studentHandInID'] = item[1]
                    if item[2]:
                        dic['score'] = float(item[2])
                    else:
                        dic['score'] = None
                    if item[3] is not None:
                        dic['content'] = 1
                    else:
                        dic['content'] = 0
                    dic['userName'] = item[4]
                    result.append(dic)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def get_a_test(cls, db_util, studenthandinId: int):
        '''
        返回试卷内容，答案，学生内容
        :param db_util:
        :param studenthandinId:
        :return:
        '''
        try:
            query = f"SELECT hep.question,hep.answer,shi.content FROM student_hand_in shi,homework_or_exam hp,homework_or_exam_pool hep WHERE shi.homeworkExamID=hp.heID and hp.homeworkExamPoolID=hep.hepID and shi.studenthandinID=%s"
            conn = db_util.get_connection()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (studenthandinId,))
                    ans = cursor.fetchall()
            finally:
                conn.close()
            data = dict()
            result = TeacherUtils.getPaperForShowWithoutAnswer(studenthandinId, db_util)
            answer = json.loads(ans[0][1])
            content = json.loads(ans[0][2])
            data['answer'] = answer
            data['studentContent'] = content
            data['question'] = result['questions']
            data['subject'] = result['subject']
            data['main_content'] = result['main_content']
            return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def change_score(cls, db_util, studenthandinId: int, scores: list):
        try:
            dao = StudentHandInDAO(db_util)
            resultset = dao.query(studenthandinId)
            total = 0
            details = json.loads(getattr(resultset, 'resultDetails'))
            total += details['判断题得分']
            total += details['选择题得分']
            cnt1 = 0
            cnt2 = 0
            total1 = 0
            total2 = 0
            scores1 = scores[0]
            scores2 = scores[1]
            for score in scores1:
                total1 += score[0]
                cnt1 += 1
            for score in scores2:
                total2 += score[0]
                cnt2 += 1
            total += total1 + total2
            details['填空题得分'] = total1
            details['填空题总个数'] = cnt1
            details['主观题得分'] = total2
            details['主观题总个数'] = cnt2
            details['试卷总分数'] = total
            setattr(resultset, 'resultDetails', details)
            setattr(resultset, 'score', total)
            dao.update(studenthandinId, resultset)
            return '试卷总分已汇总'
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def get_dati_analysis(cls, db_util, studenthandinId: int):
        try:
            dao = StudentHandInDAO(db_util)
            resultset = dao.query(studenthandinId)
            details = json.loads(getattr(resultset, 'resultDetails'))
            data = {}
            data['选择题']['总分'] = details['选择题总分']
            data['选择题']['得分'] = details['选择题得分']
            data['判断题']['总分'] = details['判断题总分']
            data['判断题']['得分'] = details['判断题得分']
            data['填空题']['总分'] = details['填空题总分']
            data['填空题']['得分'] = details['填空题得分']
            data['主观题']['总分'] = details['主观题总分']
            data['主观题']['得分'] = details['主观题得分']
            data['总体']['总分'] = details['试卷总分']
            data['总体']['得分'] = details['试卷得分']
            line = Line()

            x_data = list(details.keys())

            line.add_xaxis(x_data)
            line.add_yaxis("得分", [detail['得分'] for detail in details.values()])
            line.add_yaxis("总分", [detail['总分'] for detail in details.values()])

            line.set_global_opts(
                title_opts=TitleOpts(title="成绩报告"),
                legend_opts=LegendOpts(pos_top="5%", pos_left="left"),
                toolbox_opts=ToolboxOpts(pos_top="5%", pos_left="right")
            )
            string_html = line.render_embed()
            return string_html
        except Exception as e:
            print(e)
            return 'error'