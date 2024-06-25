import json
from datetime import datetime

import plotly.graph_objects as go
from plotly.offline import plot
from exam_sys_proj.dao.HomeworkOrExamDAO import HomeworkOrExamDAO
from exam_sys_proj.dao.HomeworkOrExamPoolDAO import HomeworkOrExamPoolDAO
from exam_sys_proj.dao.StudentCourseDAO import StudentCourseDAO
from exam_sys_proj.dao.StudentHandInDAO import StudentHandInDAO
from exam_sys_proj.orm.HomeworkOrExam import HomeworkOrExam
from exam_sys_proj.orm.StudentHandIn import StudentHandIn


class HomeworkOrExamUtils:
    @classmethod
    def insert_homeworkOrexam(cls, db_util, hepID: int, courseID: int, startTime: datetime, endTime: datetime,
                              duringTime: int):
        '''
        插入试卷ID,班级ID，发布时间，截止时间，考试时长
        :param examID:
        :param courseID:
        :param starttime:
        :param endtime:
        :param examtime:
        :return:
        '''
        try:
            homeworkexamdao = HomeworkOrExamDAO(db_util)
            homeworkexam = HomeworkOrExam()
            setattr(homeworkexam, 'homeworkExamPoolID', hepID)
            setattr(homeworkexam, 'courseID', courseID)
            setattr(homeworkexam, 'startTime', startTime)
            setattr(homeworkexam, 'endTime', endTime)
            setattr(homeworkexam, 'duringTime', duringTime)
            pri = homeworkexamdao.insert(homeworkexam)
            studentcoursedao = StudentCourseDAO(db_util)
            result = studentcoursedao.query(courseID, 'courseID', 1)
            lis = []
            for item in result:
                lis.append(getattr(item, 'userID'))
            ans = []
            for item in lis:
                entity = StudentHandIn()
                setattr(entity, 'userID', item)
                setattr(entity, 'homeworkExamID', pri)
                setattr(entity, 'createTime', startTime)
                ans.append(entity)
            studenthandindao = StudentHandInDAO(db_util)
            studenthandindao.batchInsert(ans)
            return '试卷发布成功'
        except  Exception as e:
            print(e)
            return 'error'

    @classmethod
    def testresult_analysis(cls, db_util, heID: int):
        '''
        某张试卷所有答题分数情况的分析
        目前调用函数即跳转浏览器用Jupyter NoteBook渲染
        :param db_util:
        :param heID:
        :return:
        '''
        try:
            homeworkexam = HomeworkOrExamDAO(db_util)
            test = homeworkexam.query(heID)
            data = getattr(test, 'result')
            if getattr(test, 'result') is None:
                dao = StudentHandInDAO(db_util)
                resultset = dao.query(heID, 'homeworkExamID', 1)
                scores = []
                for item in resultset:
                    if getattr(item, 'score') is None:
                        continue
                    scores.append(float(getattr(item, 'score')))
                scores.sort(reverse=True)
                mx = max(scores)
                mn = min(scores)
                cnt = len(scores)
                total = sum(scores)
                avg = total / cnt
                data = dict()
                data['分数'] = scores
                data['有效总人数'] = cnt
                data['最高分'] = mx
                data['最低分'] = mn
                data['平均分'] = avg
                lis = []
                for i in range(min(cnt, len(scores))):
                    lis.append(scores[i])
                data['分数最高的10个成绩'] = lis
                pool = HomeworkOrExamPoolDAO(db_util)
                result = pool.query(getattr(test, 'homeworkExamPoolID'), 'hepID')
                total = 0
                for item in json.loads(getattr(result, 'question'))['score']:
                    # print(item)
                    for now in item:
                        # print(type(now))
                        if isinstance(now, float):
                            total = total + now
                        else:
                            for value in now:
                                total = total + value
                data['满分'] = total
                setattr(test, 'result', json.dumps(data, ensure_ascii=False))
                homeworkexam.update(test, heID)
            else:
                data = json.loads(data)
            # {"分数": [14.5, 13.5, 9.8, 2.5], "满分": 18.5, "平均分": 10.075, "最低分": 2.5, "最高分": 14.5,
            #  "有效总人数": 4, "分数最高的10个成绩": [14.5, 13.5, 9.8, 2.5]}

            fig = go.Figure()
            score_intervals = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]
            score_counts = [0] * len(score_intervals)

            for score in data['分数']:
                score = int(100 * score / data['满分'])
                for i in range(len(score_intervals) - 1):
                    if score_intervals[i] <= score < score_intervals[i + 1]:
                        score_counts[i] += 1
                        break

            fig.add_trace(go.Bar(
                x=[f'{score_intervals[i]}-{score_intervals[i + 1] - 1}' for i in range(len(score_intervals) - 1)],
                y=score_counts,
                marker_color='pink'
            ))

            fig.update_layout(
                title={
                    'text': '成绩分布',
                    'font': {
                        'color': 'blue',  # 设置标题颜色为蓝色
                        'size': 20  # 设置标题字体大小为20
                    }
                },
                xaxis_title='成绩区间百分比',
                yaxis_title={
                    'text': '人数',
                    'font': {
                        'color': 'green',  # 设置标题颜色为蓝色
                        'size': 15  # 设置标题字体大小为20
                    }
                },
                annotations=[
                    dict(
                        x=1.05,
                        y=1,
                        xref="paper",
                        yref="paper",
                        text=f"<b><span style='color:orange'>试卷满分:{data['满分']} 有效总人数: {data['有效总人数']}  最高分: {data['最高分']}  最低分: {data['最低分']}  平均分: {data['平均分']}</span></b>",
                        showarrow=False,
                        align="left",
                        font=dict(
                            size=12
                        )
                    )
                ]
            )
            fig.show()
            # html_string = plot(fig, output_type='div')
            # return html_string
        except Exception as e:
            print(e)
            return 'error'
