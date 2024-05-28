
class BroadcastShow:
    def __init__(self, broadcastShowID=None, userID=None, broadcastID=None, isActive=None):
        self.broadcastShowID = broadcastShowID
        self.userID = userID
        self.broadcastID = broadcastID
        self.isActive = isActive

    @property
    def broadcastShowID(self):
        return self._broadcastShowID

    @broadcastShowID.setter
    def broadcastShowID(self, value):
        self._broadcastShowID = value

    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, value):
        self._userID = value

    @property
    def broadcastID(self):
        return self._broadcastID

    @broadcastID.setter
    def broadcastID(self, value):
        self._broadcastID = value

    @property
    def isActive(self):
        return self._isActive

    @isActive.setter
    def isActive(self, value):
        self._isActive = value
