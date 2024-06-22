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

            lis = json.loads(data['content'])
            answer = json.loads(ans[0][2])
            test = json.loads(ans[0][1])['questions']

            pos = 0
            details = {}
            if '主观题' in test.keys():
                cnt = len(test['主观题']) - 1
                pos = pos + cnt
            if '判断题' in test.keys():
                score = 0
                cnt = len(test['判断题']) - 1
                correct = 0
                for i in range(pos, pos + cnt):
                    if lis[i][0] == answer[i][0]:
                        score = score + test['判断题'][0]
                        correct += 1
                pos = pos + cnt
                details['判断题得分'] = score
                details['判断题回答正确个数'] = correct
                details['判断题总个数'] = cnt
            if '填空题' in test.keys():
                cnt = len(test['填空题']) - 1
                pos = pos + cnt
            if '选择题' in test.keys():
                cnt = len(test['选择题']) - 1
                score = 0
                correct = 0
                for i in range(pos, pos + cnt):
                    if lis[i][0] == answer[i][0]:
                        score = score + test['选择题'][0]
                        correct += 1
                pos = pos + cnt
                details['选择题得分'] = score
                details['选择题回答正确个数'] = correct
                details['选择题总个数'] = cnt
            setattr(result, 'resultDetails', json.dumps(details))
            dao.update(result, studenthandinId)
            return '选择题和判断题批改成功'
        except Exception as e:
            print(e)
            return 'error'
