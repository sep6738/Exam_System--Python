
class Broadcast:
    def __init__(self, broadcastID=None, content=None, duringTime=None, courseID=None):
        self.broadcastID = broadcastID
        self.content = content
        self.duringTime = duringTime
        self.courseID = courseID

    @property
    def broadcastID(self):
        return self._broadcastID

    @broadcastID.setter
    def broadcastID(self, value):
        self._broadcastID = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def duringTime(self):
        return self._duringTime

    @duringTime.setter
    def duringTime(self, value):
        self._duringTime = value

    @property
    def courseID(self):
        return self._courseID

    @courseID.setter
    def courseID(self, value):
        self._courseID = value
