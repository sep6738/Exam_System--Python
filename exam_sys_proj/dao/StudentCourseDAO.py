from orm.StudentCourse import StudentCourse
from .base_dao import BaseDAO


class StudentCourseDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, StudentCourse, "student_course", "scID")