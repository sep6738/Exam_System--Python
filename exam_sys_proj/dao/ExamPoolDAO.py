from ..orm.ExamPool import ExamPool
from .base_dao import BaseDAO


class ExamPoolDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, ExamPool, "exam_pool", "epID")