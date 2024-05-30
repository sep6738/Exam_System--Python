from ..orm.TeacherCourse import TeacherCourse
from .base_dao import BaseDAO


class TeacherCourseDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, TeacherCourse, "teacher_course", "courseID")