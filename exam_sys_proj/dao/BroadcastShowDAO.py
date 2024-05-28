from orm.BroadcastShow import BroadcastShow
from .base_dao import BaseDAO


class BroadcastShowDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, BroadcastShow, "broadcast_show", "broadcastShowID")