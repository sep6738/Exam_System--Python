from ..orm.HomeworkOrExamPool import HomeworkOrExamPool
from .base_dao import BaseDAO


class HomeworkOrExamPoolDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, HomeworkOrExamPool, "homework_or_exam_pool", "hepID")