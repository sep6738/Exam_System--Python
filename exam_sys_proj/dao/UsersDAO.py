from ..orm.Users import Users
from .base_dao import BaseDAO


class UsersDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Users, "users", "userID")

    def QueryViaEmail(self, email):
        """
        根据邮箱查询密码hash(bytes类型)
        若查到则返回密码hash(bytes类型)
        若没查到则返回"noResult"字符串
        查询错误返回"error"字符串
        :param email:
        :return:Users的一个对象
        """
        try:
            columns = [attr for attr in dir(self.entity_class) if not callable(getattr(self.entity_class, attr)) and not attr.startswith("_")]
            query = f"SELECT {', '.join(columns)} FROM {self.table_name} WHERE email = %s"
            result = self.execute_query(query, (email,))
            if result:
                return self._create_entity_from_row(result[0])
            return "noResult"
        except Exception as e:
            print(e)
            return "error"




