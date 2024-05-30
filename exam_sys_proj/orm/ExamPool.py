
class ExamPool:
    def __init__(self, epID=None, examID=None, questionID=None, questionNumber=None):
        self.epID = epID
        self.examID = examID
        self.questionID = questionID
        self.questionNumber = questionNumber

    @property
    def epID(self):
        return self._epID

    @epID.setter
    def epID(self, value):
        self._epID = value

    @property
    def examID(self):
        return self._examID

    @examID.setter
    def examID(self, value):
        self._examID = value

    @property
    def questionID(self):
        return self._questionID

    @questionID.setter
    def questionID(self, value):
        self._questionID = value

    @property
    def questionNumber(self):
        return self._questionNumber

    @questionNumber.setter
    def questionNumber(self, value):
        self._questionNumber = value
