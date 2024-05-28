from orm.Users import Users
from .base_dao import BaseDAO


class UsersDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Users, "users", "userID")