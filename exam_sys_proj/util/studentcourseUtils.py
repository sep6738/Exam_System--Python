
from exam_sys_proj.dao.StudentCourseDAO import StudentCourseDAO
from exam_sys_proj.dao.TeacherCourseDAO import TeacherCourseDAO
from exam_sys_proj.orm.StudentCourse import StudentCourse
from exam_sys_proj.orm.TeacherCourse import TeacherCourse


class StudentCourseUtils:
    @classmethod
    def insert_course_student(cls,db_util,courseID:int,userID:int):
        '''
        班级里添加学生
        :param db_util:
        :param courseID:
        :param userID:
        :return:
        '''
        try:
            teachercoursedao = TeacherCourseDAO(db_util)
            result = teachercoursedao.query(courseID,'courseID')
            teachercourse = TeacherCourse()
            columns = [attr for attr in dir(teachercourse) if not callable(getattr(teachercourse, attr)) and not attr.startswith("_")]
            data = dict()
            if result is not None:
                for attr in columns:
                    data[attr] = getattr(result, attr)
            # for row in columns:
            #     print(row)
            data['userID'] = userID
            studentcoursedao = StudentCourseDAO(db_util)
            studentcourse = StudentCourse()
            course = [attr for attr in dir(studentcourse) if not callable(getattr(studentcourse, attr)) and not attr.startswith("_")]
            for attr in course:
                if attr in data:
                    setattr(studentcourse, attr, data[attr])
            studentcoursedao.insert(studentcourse)
            return '插入成功'
            # print(data)
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def delete_course_student(cls, db_util, courseID: int, userID: int):
        '''
        从班级里删除学生
        :param db_util:
        :param courseID:
        :param userID:
        :return:
        '''
        try:
            studentcoursedao = StudentCourseDAO(db_util)
            query = f"SELECT scID FROM {studentcoursedao.table_name} WHERE courseID = {courseID} AND userID = {userID}"
            result = studentcoursedao.execute_query(query)
            if result is not None:
                scID = result[0]
                studentcoursedao.delete(scID)
                return '删除成功'
            else:
                return '班级里不存在该学生'
        except Exception as e:
            print(e)
            return 'error'

    @classmethod
    def get_student_grade(cls, db_util,userID: int,semester):
        '''
        获得学生在某个学期的学科与成绩
        :param db_util:
        :param userID:
        :param semester:
        :return:
        '''
        try:
            query = f"SELECT student_course.userID,subject,grade FROM student_course,teacher_course WHERE student_course.courseID=teacher_course.courseID and student_course.semester=%s AND student_course.userID={userID}"
            conn = db_util.get_connection()
            params = semester
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    result = cursor.fetchall()
            finally:
                conn.close()
            data = []
            for item in result:
                now = {}
                now['userID'] = item[0]
                now['subject'] = item[1]
                now['grade'] = float(item[2])
                data.append(now)
            return data
        except Exception as e:
            print(e)
            return 'error'