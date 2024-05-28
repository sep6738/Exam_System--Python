
class HepAndKpMediater:
    def __init__(self, mediaterID=None, hepID=None, kpID=None):
        self.mediaterID = mediaterID
        self.hepID = hepID
        self.kpID = kpID

    @property
    def mediaterID(self):
        return self._mediaterID

    @mediaterID.setter
    def mediaterID(self, value):
        self._mediaterID = value

    @property
    def hepID(self):
        return self._hepID

    @hepID.setter
    def hepID(self, value):
        self._hepID = value

    @property
    def kpID(self):
        return self._kpID

    @kpID.setter
    def kpID(self, value):
        self._kpID = value
