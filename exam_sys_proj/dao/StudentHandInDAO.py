from orm.StudentHandIn import StudentHandIn
from .base_dao import BaseDAO


class StudentHandInDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, StudentHandIn, "student_hand_in", "studentHandInID")
