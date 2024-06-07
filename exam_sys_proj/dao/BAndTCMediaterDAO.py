from ..orm.BAndTCMediater import BAndTCMediater
from .base_dao import BaseDAO


class BAndTCMediaterDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, BAndTCMediater, "b_and_tc_mediater", "mediaterID")
