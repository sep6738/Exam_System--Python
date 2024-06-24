from datetime import datetime

from exam_sys_proj.dao.ExamPoolDAO import ExamPoolDAO
from exam_sys_proj.dao.HomeworkOrExamDAO import HomeworkOrExamDAO
from exam_sys_proj.dao.StudentCourseDAO import StudentCourseDAO
from exam_sys_proj.dao.StudentHandInDAO import StudentHandInDAO
from exam_sys_proj.orm.HomeworkOrExam import HomeworkOrExam
from exam_sys_proj.orm.StudentHandIn import StudentHandIn


class HomeworkOrExamUtils:
    @classmethod
    def insert_homeworkOrexam(cls, db_util, hepID: int, courseID: int, startTime: datetime, endTime: datetime, duringTime: int):
        '''
        插入试卷ID,班级ID，发布时间，截止时间，考试时长
        :param examID:
        :param courseID:
        :param starttime:
        :param endtime:
        :param examtime:
        :return:
        '''
        try:
            homeworkexamdao = HomeworkOrExamDAO(db_util)
            homeworkexam = HomeworkOrExam()
            setattr(homeworkexam, 'homeworkExamPoolID', hepID)
            setattr(homeworkexam, 'courseID', courseID)
            setattr(homeworkexam, 'startTime', startTime)
            setattr(homeworkexam, 'endTime', endTime)
            setattr(homeworkexam, 'duringTime', duringTime)
            pri = homeworkexamdao.insert(homeworkexam)
            studentcoursedao = StudentCourseDAO(db_util)
            result = studentcoursedao.query(courseID, 'courseID', 1)
            lis = []
            for item in result:
                lis.append(getattr(item, 'userID'))
            ans = []
            for item in lis:
                entity = StudentHandIn()
                setattr(entity, 'userID', item)
                setattr(entity, 'homeworkExamID', pri)
                setattr(entity, 'createTime', startTime)
                ans.append(entity)
            studenthandindao = StudentHandInDAO(db_util)
            studenthandindao.batchInsert(ans)
            return '试卷发布成功'
        except  Exception as e:
            print(e)
            return 'error'