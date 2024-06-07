class BAndTCMediater:
    def __init__(self, mediaterID=None, broadcastID=None, courseID=None):
        self.mediaterID = mediaterID
        self.broadcastID = broadcastID
        self.courseID = courseID

    @property
    def mediaterID(self):
        return self._mediaterID

    @mediaterID.setter
    def mediaterID(self, value):
        self._mediaterID = value

    @property
    def broadcastID(self):
        return self._broadcastID

    @broadcastID.setter
    def broadcastID(self, value):
        self._broadcastID = value

    @property
    def courseID(self):
        return self._courseID

    @courseID.setter
    def courseID(self, value):
        self._courseID = value
