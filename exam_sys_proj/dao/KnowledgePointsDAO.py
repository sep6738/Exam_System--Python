from orm.KnowledgePoints import KnowledgePoints
from .base_dao import BaseDAO


class KnowledgePointsDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, KnowledgePoints, "knowledge_points", "kpID")