from ..orm.RegistrationCode import RegistrationCode
from .base_dao import BaseDAO


class RegistrationCodeDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, RegistrationCode, "registration_code", "email")

    def SetVerificationCode(self, entity: RegistrationCode, email):
        """
        根据email插入验证码和验证码过期时间
        先检查是否存在email
        若存在则更新数据，不存在则插入数据
        :param entity:
        :return:
        """
        # 查询是否存在email
        try:
            columns = ["verificationCode", "expirationDate"]
            query = f"SELECT {', '.join(columns)} FROM {self.table_name} WHERE {self.primary_key} = %s"
            result = self.execute_query(query, (email,))
            # 若存在则更新数据
            if result:
                set_clause = "verificationCode = %s, expirationDate = %s"
                query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary_key} = %s"
                values = [entity.verificationCode, entity.expirationDate, email]
                self.execute_update(query, values)
            # 不存在则插入
            else:
                columns.append(self.primary_key)
                placeholders = ", ".join(["%s"] * len(columns))
                query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                values = [entity.verificationCode, entity.expirationDate, email]
                self.execute_update(query, values)
        except Exception as e:
            print(e)

