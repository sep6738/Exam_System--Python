from .StudentCourseDAO import StudentCourseDAO
from ..orm.Broadcast import Broadcast
from .base_dao import BaseDAO
from ..orm.StudentCourse import StudentCourse
from ..util.db_util import DBUtil


class BroadcastDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Broadcast, "broadcast", "broadcastID")

    def select_broadcast_by_broadcastid(self, k_id_list: list):
        '''
        传入要查询的广播ID列表，将查询到的每条广播信息封装成orm对象，再返回orm对象组成的列表
        :param k_id_list:
        :return:
        '''
        try:
            placeholders = ", ".join(["%s"] * len(k_id_list))
            columns = [attr for attr in dir(self.entity_class) if
                       not callable(getattr(self.entity_class, attr)) and not attr.startswith("_")]
            query = f"SELECT {', '.join(columns)} FROM {self.table_name} WHERE broadcastid IN ({placeholders})"
            result = self.execute_query(query, k_id_list)
            result_list = []
            for row in result:
                result_list.append(self._create_entity_from_row(row))
            return result_list
        except Exception as e:
            print(e)
            return "error"
    def get_broadcastid_to_userid(self,broadcast_id : int):
        '''
        传入要查询的广播ID,查找courseID，进而查找所有在该courseID中的userid
        注意:返回值是一个userid组成的列表，不是orm封装对象
        :param broadcast_id:
        :return:
        '''
        try:
            query = f"SELECT courseID FROM {self.table_name} WHERE broadcastid =%s"
            result = self.execute_query(query, (broadcast_id,))
            if result:
                course_id = result[0][0]
                db_util = DBUtil()
                studentcoursedao  = StudentCourseDAO(db_util)
                ans = studentcoursedao.query(course_id,'courseID',1)
                lis = []
                for i in ans:
                    lis.append(getattr(i,'userID'))
                return lis
            else:
                return "noResult"
        except Exception as e:
            print(e)
            return "error"