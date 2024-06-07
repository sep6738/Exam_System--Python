import json


class HomeworkOrExamPool:
    def __init__(self, hepID=None, type=None, question=None, answer=None, courseName=None, difficultyLevel=None,
                 isActive=None):
        self.hepID = hepID
        self.type = type
        self.question = question
        self.answer = answer
        self.courseName = courseName
        self.difficultyLevel = difficultyLevel
        self.isActive = isActive

    @property
    def hepID(self):
        return self._hepID

    @hepID.setter
    def hepID(self, value):
        self._hepID = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, value):
        try:
            if isinstance(value, list) or isinstance(value, dict):
                self._question = json.dumps(value)
            else:
                self._question = value
        except Exception as e:
            print(e)
            self._question = json.dumps(list())

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value):
        try:
            if isinstance(value, list) or isinstance(value, dict):
                self._answer = json.dumps(value)
            else:
                self._answer = value
        except Exception as e:
            print(e)
            self._answer = json.dumps(list())

    @property
    def courseName(self):
        return self._courseName

    @courseName.setter
    def courseName(self, value):
        self._courseName = value

    @property
    def difficultyLevel(self):
        return self._difficultyLevel

    @difficultyLevel.setter
    def difficultyLevel(self, value):
        self._difficultyLevel = value

    @property
    def isActive(self):
        return self._isActive

    @isActive.setter
    def isActive(self, value):
        self._isActive = value
