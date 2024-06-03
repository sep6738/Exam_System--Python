from ..dao.HomeworkOrExamPoolDAO import HomeworkOrExamPool, HomeworkOrExamPoolDAO
from ..dao.KnowledgePointsDAO import KnowledgePointsDAO, KnowledgePoints
from ..dao.HepAndKpMediaterDAO import HepAndKpMediater, HepAndKpMediaterDAO
from ..dao.TeacherCourseDAO import TeacherCourse, TeacherCourseDAO
import json


class TeacherUtils:
    @classmethod
    def insertOneQuestion(cls, db_util, question_dict: dict):
        homeworkOrExamPoolDao = HomeworkOrExamPoolDAO(db_util)
        hepAndKpMediaterDAO = HepAndKpMediaterDAO(db_util)
        homeworkOrExamPool = HomeworkOrExamPool(
            type=question_dict["type"],
            answer=question_dict["answer"],
            courseName=question_dict['subject'],
            difficultyLevel=question_dict['difficulty'],
            isActive=True
        )
        # knowledgePoints = KnowledgePoints(
        #     subject=question_dict['subject']
        # )
        kp_list = []
        for i in question_dict['knowledge_point']:
            kp_list.append(int(i))
        del question_dict["answer"]
        del question_dict['knowledge_point']
        del question_dict['difficulty']
        del question_dict['subject']
        homeworkOrExamPool.question = json.dumps(question_dict)
        hepID = homeworkOrExamPoolDao.insert(homeworkOrExamPool)
        print(kp_list, 5)
        if len(kp_list) > 0:
            for i in kp_list:
                hepAndKpMediater = HepAndKpMediater(hepID=hepID, kpID=i)
                hepAndKpMediaterDAO.insert(hepAndKpMediater)



    @classmethod
    def queryTeacherSubjectKP(cls, db_util, userID: int):
        """
        传入dbutil初始化，传入教师的userID进行查询，返回一个元素是“KnowledgePoints类的orm对象”的list
        :param db_util:
        :param userID:
        :return : 元素是knowledgePoints的orm的list
        """
        teacherCourseDAO = TeacherCourseDAO(db_util)
        knowledgePointsDAO = KnowledgePointsDAO(db_util)
        subject_list = teacherCourseDAO.querySubjectViaTeacherID(userID)
        result_list = knowledgePointsDAO.query(value=subject_list[0].subject, column_name="subject",  is_all=True)
        return result_list
