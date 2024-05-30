class Role:
    def __init__(self, roleID=None, roleName=None):
        self.roleID = roleID
        self.roleName = roleName

    @property
    def roleID(self):
        return self._roleID

    @roleID.setter
    def roleID(self, value):
        self._roleID = value

    @property
    def roleName(self):
        return self._roleName

    @roleName.setter
    def roleName(self, value):
        self._roleName = value
