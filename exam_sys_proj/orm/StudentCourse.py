class StudentCourse:
    def __init__(self, scID=None, courseName=None, userID=None, semester=None, time=None, grade=None, courseID=None,
                 isDelete=None):
        self.scID = scID
        self.courseName = courseName
        self.userID = userID
        self.semester = semester
        self.time = time
        self.grade = grade
        self.courseID = courseID
        self.isDelete = isDelete

    @property
    def scID(self):
        return self._scID

    @scID.setter
    def scID(self, value):
        self._scID = value

    @property
    def courseName(self):
        return self._courseName

    @courseName.setter
    def courseName(self, value):
        self._courseName = value

    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, value):
        self._userID = value

    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self, value):
        self._semester = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        self._grade = value

    @property
    def courseID(self):
        return self._courseID

    @courseID.setter
    def courseID(self, value):
        self._courseID = value

    @property
    def isDelete(self):
        return self._isDelete

    @isDelete.setter
    def isDelete(self, value):
        self._isDelete = value
