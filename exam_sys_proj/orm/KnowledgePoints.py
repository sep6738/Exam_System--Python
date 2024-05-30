
class KnowledgePoints:
    def __init__(self, kpID=None, kpName=None, subject=None):
        self.kpID = kpID
        self.kpName = kpName
        self.subject = subject

    @property
    def kpID(self):
        return self._kpID

    @kpID.setter
    def kpID(self, value):
        self._kpID = value

    @property
    def kpName(self):
        return self._kpName

    @kpName.setter
    def kpName(self, value):
        self._kpName = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value
