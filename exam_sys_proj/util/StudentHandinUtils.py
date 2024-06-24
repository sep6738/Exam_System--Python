import json

from exam_sys_proj.dao.StudentHandInDAO import StudentHandInDAO
from exam_sys_proj.orm.StudentHandIn import StudentHandIn


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
                details['判断题得分'] = score
                details['判断题回答正确个数'] = correct
                details['判断题总个数'] = cnt
            setattr(result, 'resultDetails', json.dumps(details, ensure_ascii=False))
            dao.update(result, studenthandinId)
            return '选择题和判断题批改成功'
        except Exception as e:
            print(e)
            return 'error'

    # 以下为自测试卷
    @classmethod
    def insert_self_exam(cls, db_util, test_paper: dict, answer_list: list, userid: int):
        '''
        传入试卷的内容和答案，以及用户id，往student_hand_in表里面创建试卷，返回主键值
        :param db_util:
        :param test_paper:
        :param answer_list:
        :param userid:
        :return:
        '''
        try:
            test_paper['answer'] = answer_list
            dao = StudentHandInDAO(db_util)
            entity = StudentHandIn()
            setattr(entity, 'userID', userid)
            setattr(entity, 'testPaper', json.dumps(test_paper))
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
        试卷返回title,score,type,paperID,subject
        自测返回title,score,type,paper
        :param db_util:
        :param userID:
        :return:
        '''
        try:
            query = f"SELECT hp.homeworkExamPoolID,hep.question,hep.courseName,shi.score,hep.type FROM student_hand_in shi,homework_or_exam hp,homework_or_exam_pool hep WHERE shi.homeworkExamID=hp.heID and hp.homeworkExamPoolID=hep.hepID and shi.userID=%s and shi.homeworkExamID != -1"
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
                result.append(dic)
            studenthandindao = StudentHandInDAO(db_util)
            query_list = studenthandindao.query(-1, 'homeworkExamID', '1')
            for item in query_list:
                dic = dict()
                dic['type'] = '自测'
                question = json.loads(getattr(item, 'testPaper'))
                dic['title'] = question['main_content']
                dic['score'] = getattr(item, 'score')
                dic['paper'] = json.dumps(question, ensure_ascii=False)
                result.append(dic)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            print(e)
            return 'error'