from datetime import datetime

from exam_sys_proj.dao.ExamPoolDAO import ExamPoolDAO
from exam_sys_proj.dao.HomeworkOrExamDAO import HomeworkOrExamDAO
from exam_sys_proj.orm.HomeworkOrExam import HomeworkOrExam


class HomeworkOrExamUtils:
    @classmethod
    def insert_homeworkOrexam(cls,db_util,examID:int,courseID:int,startTime:datetime,endTime:datetime,duringTime:int):
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
            exampooldao = ExamPoolDAO(db_util)
            result = exampooldao.query(examID,'examID',1)
            lis = []
            shijuan = HomeworkOrExam()
            columns = [attr for attr in dir(shijuan) if not callable(getattr(shijuan, attr)) and not attr.startswith("_")]
            for row in result:
                now = getattr(row,'questionID')
                entity = HomeworkOrExam()
                setattr(entity,'homeworkExamPoolID',now)
                setattr(entity,'courseID',courseID)
                setattr(entity,'duringTime',duringTime)
                setattr(entity,'startTime',startTime)
                setattr(entity,'endTime',endTime)
                lis.append(entity)
            shijuandao = HomeworkOrExamDAO(db_util)
            shijuandao.batchInsert(lis,0)
            return '试卷发布成功'
        except  Exception as e:
            print(e)
            return 'error'