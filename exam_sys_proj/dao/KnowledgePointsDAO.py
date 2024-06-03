from ..orm.KnowledgePoints import KnowledgePoints
from .base_dao import BaseDAO


class KnowledgePointsDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, KnowledgePoints, "knowledge_points", "kpID")

    def knowledgeNameCheck(self, k_name_list: list):
        placeholders = ", ".join(["%s"] * len(k_name_list))
        query = f"SELECT kpName FROM {self.table_name} WHERE kpName IN ({placeholders})"
        result = self.execute_query(query, k_name_list)
