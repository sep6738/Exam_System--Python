from .StudentCourseDAO import StudentCourseDAO
from ..orm.TeacherCourse import TeacherCourse
from .base_dao import BaseDAO
from ..util.db_util import DBUtil
import pandas as pd
from matplotlib import pyplot as plt


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

    def getScoreanalysis(self, courseID: int):
        '''
        传入courseID，返回图片的相对路径，可以呈现对应courseID的成绩分布饼状图
        :param courseID:
        :return:图片相对路径
        '''
        db_util = DBUtil()
        studentcoursedao = StudentCourseDAO(db_util)
        try:
            result = studentcoursedao.query(courseID, 'CourseID', 1)
            data = {'userid': [], 'grade': []}
            for row in result:
                data['userid'].append(getattr(row, 'userID'))
                data['grade'].append(getattr(row, 'grade'))
            df = pd.DataFrame(data)
            df.set_index("userid", inplace=True)
            for x in df.index:
                if df.loc[x, 'grade'] is None:
                    df.loc[x, "grade"] = 0

            num = pd.cut(df['grade'], bins=[0, 60, 70, 80, 90, 100],
                         labels=['0-59', '60-69', '70-79', '80-89', '90-100'],
                         right=False)
            counts = num.value_counts(sort=False)
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文字体
            plt.pie(counts, autopct='%1.1f%%')  # autopct后面的值1.1表示保留2位小数
            plt.legend(labels=['0-59', '60-69', '70-79', '80-89', '90-100'], loc="best")
            plt.title("学生成绩区间分布图")
            file_name = r".\img\{name}.png"
            path = file_name.format(name=courseID)
            plt.savefig(path)
            return path
        except Exception as e:
            print(e)
            return 'error'
