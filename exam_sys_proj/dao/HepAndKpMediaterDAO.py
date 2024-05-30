from ..orm.HepAndKpMediater import HepAndKpMediater
from .base_dao import BaseDAO


class HepAndKpMediaterDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, HepAndKpMediater, "hep_and_kp_mediater", "mediaterID")