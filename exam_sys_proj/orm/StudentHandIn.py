class StudentHandIn:
    def __init__(self, studentHandInID=None, userID=None, homeworkExamID=None, content=None, upTime=None, score=None,
                 teacherComment=None, resultDetails=None ,testPaper=None, createTime=None):
        self.studentHandInID = studentHandInID
        self.userID = userID
        self.homeworkExamID = homeworkExamID
        self.content = content
        self.upTime = upTime
        self.score = score
        self.teacherComment = teacherComment
        self.resultDetails = resultDetails
        self.testPaper = testPaper
        self.createTime = createTime

    @property
    def studentHandInID(self):
        return self._studentHandInID

    @studentHandInID.setter
    def studentHandInID(self, value):
        self._studentHandInID = value

    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, value):
        self._userID = value

    @property
    def homeworkExamID(self):
        return self._homeworkExamID

    @homeworkExamID.setter
    def homeworkExamID(self, value):
        self._homeworkExamID = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def upTime(self):
        return self._upTime

    @upTime.setter
    def upTime(self, value):
        self._upTime = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def teacherComment(self):
        return self._teacherComment

    @teacherComment.setter
    def teacherComment(self, value):
        self._teacherComment = value

    @property
    def resultDetails(self):
        return self._resultDetails

    @resultDetails.setter
    def resultDetails(self, value):
        self._resultDetails = value

    @property
    def testPaper(self):
        return self._testPaper

    @testPaper.setter
    def testPaper(self, value):
        self._testPaper = value

    @property
    def createTime(self):
        return self._createTime

    @createTime.setter
    def createTime(self, value):
        self._createTime = value
