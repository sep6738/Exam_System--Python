class HepAndKpMediater:
    def __init__(self, mediaterID=None, hepID=None, kpName=None):
        self.mediaterID = mediaterID
        self.hepID = hepID
        self.kpName = kpName

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
    def kpName(self):
        return self._kpName

    @kpName.setter
    def kpName(self, value):
        self._kpName = value
