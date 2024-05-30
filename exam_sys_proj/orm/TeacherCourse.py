
class TeacherCourse:
    def __init__(self, courseID=None, userID=None, semester=None, time=None, courseName=None, isActive=None, class_=None):
        self.courseID = courseID
        self.userID = userID
        self.semester = semester
        self.time = time
        self.courseName = courseName
        self.isActive = isActive
        self.class_ = class_

    @property
    def courseID(self):
        return self._courseID

    @courseID.setter
    def courseID(self, value):
        self._courseID = value

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
    def courseName(self):
        return self._courseName

    @courseName.setter
    def courseName(self, value):
        self._courseName = value

    @property
    def isActive(self):
        return self._isActive

    @isActive.setter
    def isActive(self, value):
        self._isActive = value

    @property
    def class_(self):
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = value
