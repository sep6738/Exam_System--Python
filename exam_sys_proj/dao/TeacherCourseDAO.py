from ..orm.TeacherCourse import TeacherCourse
from .base_dao import BaseDAO


class TeacherCourseDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, TeacherCourse, "teacher_course", "courseID")

    def querySubjectViaTeacherID(self, userID: int):
        """
        根据教师id查询所教授的学科，去除重复项，一行数据封装在一个orm里面，将所有orm存入列表返回
        :param userID:
        :return:
        """
        value = userID
        query = f"SELECT DISTINCT subject FROM {self.table_name} WHERE userID = %s"
        result = self.execute_query(query, (value,))
        result_list = []
        attr = "subject"
        for i in result:
            entity = self.entity_class()
            setattr(entity, attr, i[0])
            result_list.append(entity)
        return result_list

