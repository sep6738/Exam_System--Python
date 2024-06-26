class HomeworkOrExam:
    def __init__(self, heID=None, courseID=None, duringTime=None, homeworkExamPoolID=None, result=None,startTime=None, endTime=None):
        self._endTime = endTime
        self._startTime = startTime
        self.heID = heID
        self.courseID = courseID
        self.duringTime = duringTime
        self.homeworkExamPoolID = homeworkExamPoolID
        self.result = result

    @property
    def heID(self):
        return self._heID

    @heID.setter
    def heID(self, value):
        self._heID = value

    @property
    def courseID(self):
        return self._courseID

    @courseID.setter
    def courseID(self, value):
        self._courseID = value

    @property
    def duringTime(self):
        return self._duringTime

    @duringTime.setter
    def duringTime(self, value):
        self._duringTime = value

    @property
    def homeworkExamPoolID(self):
        return self._homeworkExamPoolID

    @homeworkExamPoolID.setter
    def homeworkExamPoolID(self, value):
        self._homeworkExamPoolID = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def startTime(self):
        return self._startTime

    @startTime.setter
    def startTime(self, value):
        self._startTime = value

    @property
    def endTime(self):
        return self._endTime

    @endTime.setter
    def endTime(self, value):
        self._endTime = value
