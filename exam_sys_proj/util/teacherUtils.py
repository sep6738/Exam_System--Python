from ..dao.HomeworkOrExamPoolDAO import HomeworkOrExamPool, HomeworkOrExamPoolDAO
from ..dao.KnowledgePointsDAO import KnowledgePointsDAO, KnowledgePoints
import json


class TeacherUtils:
    @classmethod
    def insertOneQuestion(cls, db_util, question_dict: dict):
        homeworkOrExamPoolDao = HomeworkOrExamPoolDAO(db_util)
        knowledgePointsDAO = KnowledgePointsDAO(db_util)
        homeworkOrExamPool = HomeworkOrExamPool(
            type=question_dict["type"],
            answer=question_dict["answer"],
            courseName=question_dict['subject'],
            difficultyLevel=question_dict['difficulty'],
            isActive=True
        )
        knowledgePoints = KnowledgePoints(
            subject=question_dict['subject']
        )
        for i in question_dict['knowledge_point']:
            knowledgePoints.kpName = i
            kppk = knowledgePointsDAO.insert(knowledgePoints)
        del question_dict["answer"]
        del question_dict['knowledge_point']
        del question_dict['difficulty']
        del question_dict['subject']
        homeworkOrExamPool.question = json.dumps(question_dict)
        hoeppk = homeworkOrExamPoolDao.insert(homeworkOrExamPool)
