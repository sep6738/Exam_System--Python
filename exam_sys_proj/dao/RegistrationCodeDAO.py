from ..orm.RegistrationCode import RegistrationCode
from .base_dao import BaseDAO


class RegistrationCodeDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, RegistrationCode, "registration_code", "email")

    def InsertVerificationCode(self, entity, pk):
        """
        根据主键插入验证码和验证码创建时间
        :param entity:
        :return:
        """

        print()

