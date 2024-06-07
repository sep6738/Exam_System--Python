from .BroadcastDAO import BroadcastDAO
from ..orm.BroadcastShow import BroadcastShow
from .base_dao import BaseDAO
from ..util.db_util import DBUtil


class BroadcastShowDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, BroadcastShow, "broadcast_show", "broadcastShowID")

    def get_user_All_Broadcast(self, userID: int):
        '''
        根据用户ID来获得所有广播通知ID，再由广播通知ID来获取所有的广播信息，每条信息封装成orm对象，返回orm对象列表
        :param userID:
        :return:
        '''
        try:
            value = userID
            query = f"SELECT broadcastID FROM {self.table_name} WHERE userID = %s"
            result = self.execute_query(query, (value,))
            if result:
                broadcastid_list = []
                for i in result:
                    broadcastid_list.append(i[0])
                db_util = DBUtil()
                broadcastdao = BroadcastDAO(db_util)
                ans = broadcastdao.select_broadcast_by_broadcastid(broadcastid_list)
                return ans
            else:
                return "noResult"
        except Exception as e:
            print(e)
            return "error"
