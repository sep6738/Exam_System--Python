import bcrypt
import datetime
import random
import string

class Users:
    def __init__(self, userID=None, userName=None, passWord=None, name=None, roleID=None, createAt=None, updateAt=None, email=None, verificationCode=None, expirationDate=None):
        self.userID = userID
        self.userName = userName
        self.passWord = passWord
        self.name = name
        self.roleID = roleID
        self.createAt = createAt
        self.updateAt = updateAt
        self.email = email
        self.verificationCode = verificationCode
        self.expirationDate = expirationDate

    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, value):
        self._userID = value

    @property
    def userName(self):
        return self._userName

    @userName.setter
    def userName(self, value):
        self._userName = value

    @property
    def passWord(self):
        """
        得到用于验证的bytes类型的哈希值
        验证使用：bcrypt.checkpw(password, hashed_bytes)
        :return:hashed_bytes
        """
        if self._passWord == None:
            return None
        else:
            # 将哈希值字符串转换回字节类型
            hashed_bytes = self._passWord.encode('utf-8')
            return hashed_bytes

    @passWord.setter
    def passWord(self, value):
        """
        实现密码加密存储
        用户输入密码长度为16-20位，须在前端设置检测
        经过bcrypt算法加密后哈希字符串长度为60位
        :param value:
        :return:
        """
        # 生成盐值,成本设置为8
        salt = bcrypt.gensalt(rounds=8)
        if isinstance(value, str):
            # 若传入的字符串长度在9-20之间则认为是用户输入，加密存储
            if 9 <= len(value) <= 20:
                # 构建哈希密码
                value = value.encode("utf-8")
                hashed = bcrypt.hashpw(value, salt)
                # 将哈希值转换为字符串并存储
                hashed_str = hashed.decode('utf-8')
                self._passWord = hashed_str
            elif len(value) < 9:
                self._passWord = None
                print("密码长度小于9位")
            else:
                # 若传入字符串长度大于20，则认为传入的是加密后的哈希，不做任何处理，直接存储
                self._passWord = value
        else:
            self._passWord = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def roleID(self):
        return self._roleID

    @roleID.setter
    def roleID(self, value):
        self._roleID = value

    @property
    def createAt(self):
        return self._createAt

    @createAt.setter
    def createAt(self, value):
        self._createAt = value

    @property
    def updateAt(self):
        return self._updateAt

    @updateAt.setter
    def updateAt(self, value):
        self._updateAt = value

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
        characters = string.ascii_lowercase + string.digits
        if isinstance(value, str):
            if len(value) == 6 and all(char in characters for char in value):
                self._verificationCode = value
            else:
                self._verificationCode = ''.join(random.choice(characters) for _ in range(6))
        else:
            self._verificationCode = ''.join(random.choice(characters) for _ in range(6))

    @property
    def expirationDate(self):
        """
        自动执行+5min操作
        
        :return:
        """
        return self._expirationDate + datetime.timedelta(minutes=5)

    @expirationDate.setter
    def expirationDate(self, value):
        """
        检测传入是否是datetime.datetime类型数据，若是则保留到秒储存，若不是则自动获取当前系统时间
        :param value:
        :return:
        """
        if isinstance(value, datetime.datetime):
            self._expirationDate = value.replace(microsecond=0)
        else:
            self._expirationDate = datetime.datetime.now().replace(microsecond=0)
