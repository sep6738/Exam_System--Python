from ..orm.Broadcast import Broadcast
from .base_dao import BaseDAO


class BroadcastDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, Broadcast, "broadcast", "broadcastID")