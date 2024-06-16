import pandas as pd
from matplotlib import pyplot as plt

from exam_sys_proj.dao.StudentCourseDAO import StudentCourseDAO
from exam_sys_proj.orm.StudentCourse import StudentCourse
from exam_sys_proj.orm.Users import Users


class TeacherCourseUtils:
    @classmethod
    def getcourse_user(cls,db_util,courseID : int):
        '''
        传入courseID，得到student_course表上所有是该班级的user的所有信息
        :param courseID:
        :return: 由字典组成的列表
        '''
        try:
            student_course = StudentCourse()
            users = Users()
            column1 = [attr for attr in dir(student_course) if
                       not callable(getattr(student_course, attr)) and not attr.startswith("_")]
            column2 = [attr for attr in dir(users) if
                       not callable(getattr(users, attr)) and not attr.startswith("_")]
            columns = list(set(column1 + column2))
            columns.remove('userID')
            columns.append('users.userID')

            query = f"SELECT {', '.join(columns)} FROM student_course,users WHERE student_course.userID=users.userID and courseID=%s"
            conn = db_util.get_connection()
            params = courseID

            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
            finally:
                conn.close()

            columns.remove('users.userID')
            columns.append('userID')
            ans = []
            for row in result:
                data = dict()
                for j in range(len(columns)):
                    data[columns[j]] = row[j]
                ans.append(data)
            return ans
        except Exception as e:
            print(e)
            return 'error'
    @classmethod
    def getScoreanalysis(cls,db_util,courseID : int):
        '''
        传入courseID，返回图片的相对路径，可以呈现对应courseID的成绩分布饼状图
        :param db_util:
        :param courseID:
        :return:图片相对路径
        '''
        try:
            studentcoursedao = StudentCourseDAO(db_util)
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
