from orm.Users import Users
from .base_dao import BaseDAO


class UsersDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Users, "users", "userID")

    def QueryPasswordViaEmail(self, entity, email):
        """
        根据邮箱查询密码
        :param entity:
        :param email:
        :return:
        """
        passwordMD5 = None
        return passwordMD5

    def InsertVerificationCode(self, entity):
        """
        插入验证码
        :param entity: 
        :return: 
        """
        print()
    
    def InsertUserData(self, entity):
        """
        插入一条用户数据
        :param entity: 
        :return: 
        """
        print()
