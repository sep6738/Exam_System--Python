import datetime
import random
import string


class RegistrationCode:
    def __init__(self, email=None, verificationCode=None, expirationDate=None):
        self.email = email
        self.verificationCode = verificationCode
        self.expirationDate = expirationDate

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def verificationCode(self):
        return self._verificationCode

    @verificationCode.setter
    def verificationCode(self, value):
        """
        检测传入数据是否为只包含数字和小写字母的6位字符串
        若是则存储，否则自动生成
        :param value:
        :return:
        """
        characters = string.ascii_uppercase + string.digits
        if isinstance(value, str):
            if len(value) == 6 and all(char in characters for char in value):
                self._verificationCode = value
            else:
                self._verificationCode = ''.join(random.choice(characters) for _ in range(6))
        else:
            self._verificationCode = ''.join(random.choice(characters) for _ in range(6))

    @property
    def expirationDate(self):
        return self._expirationDate

    @expirationDate.setter
    def expirationDate(self, value):
        """
        检测传入是否是datetime.datetime类型数据，若是则保留到秒储存，若不是则自动获取当前系统时间并+5min
        :param value:
        :return:
        """
        if isinstance(value, datetime.datetime):
            self._expirationDate = value.replace(microsecond=0)
        else:
            self._expirationDate = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(minutes=5)
