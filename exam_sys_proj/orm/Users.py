
class Users:
    def __init__(self, userID=None, userName=None, passWord=None, name=None, roleID=None, createAt=None, updateAt=None):
        self.userID = userID
        self.userName = userName
        self.passWord = passWord
        self.name = name
        self.roleID = roleID
        self.createAt = createAt
        self.updateAt = updateAt

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
        return self._passWord

    @passWord.setter
    def passWord(self, value):
        self._passWord = value

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
