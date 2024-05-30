from ..orm.Users import Users
from .base_dao import BaseDAO


class UsersDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Users, "users", "userID")

    def QueryPasswordViaEmail(self, email):
        """
        根据邮箱查询密码hash(bytes类型)
        :param email:
        :return:Users的一个对象
        """

        query = f"SELECT passWord FROM {self.table_name} WHERE email = %s"
        result = self.execute_query(query, (email,))
        if result:
            entity = self.entity_class()
            entity.passWord = result[0][0]
            return entity
        return "noResult"

    def InsertVerificationCode(self, entity, pk):
        """
        根据主键插入验证码和验证码过期时间

        :param entity:
        :return:
        """
        print()

