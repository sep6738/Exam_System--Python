from ..dao.HomeworkOrExamPoolDAO import HomeworkOrExamPool, HomeworkOrExamPoolDAO
from ..dao.KnowledgePointsDAO import KnowledgePointsDAO, KnowledgePoints
from ..dao.HepAndKpMediaterDAO import HepAndKpMediater, HepAndKpMediaterDAO
from ..dao.TeacherCourseDAO import TeacherCourse, TeacherCourseDAO
import json


class TeacherUtils:

    def __init__(self):
        self.a = None

    @classmethod
    def insertOneQuestion(cls, db_util, question_dict: dict):
        """
        传入前端生成的题目字典，将题目存入数据库\n
        并没有保证插入的原子性，无法保证数据的完整性
        :param db_util:
        :param question_dict:
        :return:
        """
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
            kp_list.append(i)
        del question_dict["answer"]
        del question_dict['knowledge_point']
        del question_dict['difficulty']
        del question_dict['subject']
        homeworkOrExamPool.question = question_dict
        hepID = homeworkOrExamPoolDao.insert(homeworkOrExamPool)
        if len(kp_list) > 0:
            for i in kp_list:
                hepAndKpMediater = HepAndKpMediater(hepID=hepID, kpName=i)
                hepAndKpMediaterDAO.insert(hepAndKpMediater)

    @classmethod
    def queryTeacherSubjectKP(cls, db_util, userID: int):
        """
        通过教师的id查询教师所教授的学科的知识点
        传入dbutil初始化，传入教师的userID进行查询，返回一个元素是“KnowledgePoints类的orm对象”的list
        :param db_util:
        :param userID:
        :return : 元素是knowledgePoints的orm的list
        """
        teacherCourseDAO = TeacherCourseDAO(db_util)
        knowledgePointsDAO = KnowledgePointsDAO(db_util)
        subject_list = teacherCourseDAO.querySubjectViaTeacherID(userID)
        result_list = knowledgePointsDAO.query(value=subject_list[0].subject, column_name="subject", is_all=True)
        return result_list

    @classmethod
    def batchInsertQuestions(cls, db_util, json_path: str):
        """
        这是批量插入题目的丐版；并没有保证插入的原子性，无法保证数据的完整性
        :param db_util:
        :param json_path: json的文件路径
        :return:
        """
        try:
            question_list = cls._readOurJson(json_path=json_path)
            homeworkOrExamPoolDao = HomeworkOrExamPoolDAO(db_util)
            hepAndKpMediaterDAO = HepAndKpMediaterDAO(db_util)
            homeworkOrExamPool_list = []
            kp_list_all = []
            for question_dict in question_list:
                homeworkOrExamPool = HomeworkOrExamPool(
                    type=question_dict["type"],
                    answer=question_dict["answer"],
                    courseName=question_dict['subject'],
                    difficultyLevel=question_dict['difficulty'],
                    isActive=True
                )
                kp_list = []
                for i in question_dict['knowledge_point']:
                    kp_list.append(i)
                del question_dict["answer"]
                del question_dict['knowledge_point']
                del question_dict['difficulty']
                del question_dict['subject']
                homeworkOrExamPool.question = question_dict
                homeworkOrExamPool_list.append(homeworkOrExamPool)
                kp_list_all.append(kp_list)
            pk_list = homeworkOrExamPoolDao.batchInsert(homeworkOrExamPool_list)
            hepAndKpMediater_list = []
            for i in range(len(kp_list_all)):
                if len(kp_list_all[i]) > 0:
                    for j in kp_list_all[i]:
                        hepAndKpMediater = HepAndKpMediater(hepID=pk_list[i], kpName=j)
                        hepAndKpMediater_list.append(hepAndKpMediater)
            hepAndKpMediaterDAO.batchInsert(hepAndKpMediater_list)
        except Exception as e:
            print(e)
            print("batchInsertQuestions error!")
            return "error"

    # @classmethod
    # def batchInsertQuestionsTest(cls, db_util, json_path: str):
    #     """
    #     这是批量插入题目的丐版；并没有保证插入的原子性，无法保证数据的完整性
    #     :param db_util:
    #     :param json_path: json的文件路径
    #     :return:
    #     """
    #
    #     question_list = cls._readOurJson(json_path=json_path)
    #     homeworkOrExamPoolDao = HomeworkOrExamPoolDAO(db_util)
    #     hepAndKpMediaterDAO = HepAndKpMediaterDAO(db_util)
    #     homeworkOrExamPool_list = []
    #     kp_list_all = []
    #     print(question_list, -1)
    #     for question_dict in question_list:
    #         homeworkOrExamPool = HomeworkOrExamPool(
    #             type=question_dict["type"],
    #             answer=json.dumps(question_dict["answer"]),
    #             courseName=question_dict['subject'],
    #             difficultyLevel=question_dict['difficulty'],
    #             isActive=True
    #         )
    #         kp_list = []
    #         for i in question_dict['knowledge_point']:
    #             kp_list.append(int(i))
    #         del question_dict["answer"]
    #         del question_dict['knowledge_point']
    #         del question_dict['difficulty']
    #         del question_dict['subject']
    #         homeworkOrExamPool.question = json.dumps(question_dict)
    #         homeworkOrExamPool_list.append(homeworkOrExamPool)
    #         kp_list_all.append(kp_list)
    #         print(vars(homeworkOrExamPool), 000)
    #     print(homeworkOrExamPool_list, 111)
    #     pk_list = homeworkOrExamPoolDao.batchInsert(homeworkOrExamPool_list)
    #     print(pk_list, 222)
    #     hepAndKpMediater_list = []
    #     for i in range(len(kp_list_all)):
    #         if len(kp_list_all[i]) > 0:
    #             for j in kp_list_all[i]:
    #                 hepAndKpMediater = HepAndKpMediater(hepID=pk_list[i], kpName=j)
    #                 hepAndKpMediater_list.append(hepAndKpMediater)
    #     print(hepAndKpMediater_list, 333)
    #     hepAndKpMediaterDAO.batchInsert(hepAndKpMediater_list)
    #     print(666)
    #     # except Exception as e:
    #     #     print(e)
    #     #     print("batchInsertQuestions error!")
    #     #     return "error"

    @classmethod
    def querySubjectQuestionsViaUID(cls, db_util, userID, entity):
        pass

    @staticmethod
    def _readOurJson(json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            t = json.load(f)
        return t
