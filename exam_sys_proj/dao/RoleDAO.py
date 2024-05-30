from ..orm.Role import Role
from .base_dao import BaseDAO


class RoleDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Role, "role", "roleID")