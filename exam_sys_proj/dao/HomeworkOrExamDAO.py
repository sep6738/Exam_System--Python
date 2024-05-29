from ..orm.HomeworkOrExam import HomeworkOrExam
from .base_dao import BaseDAO


class HomeworkOrExamDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, HomeworkOrExam, "homework_or_exam", "heID")