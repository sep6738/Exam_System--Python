from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

from ..orm.HomeworkOrExamPool import HomeworkOrExamPool
from .base_dao import BaseDAO
import json


class HomeworkOrExamPoolDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, HomeworkOrExamPool, "homework_or_exam_pool", "hepID")


    def query_whole_paper(self, store_paper: dict):
        # 解析字典
        questions_list = []
        answer_list = []
        diff_list = []
        question_type_list = []
        for question_type in store_paper["questions"]:
            question_type_list.append(question_type)
            if len(tuple(store_paper["questions"][question_type][1:])) > 1:
                pl = str(tuple(store_paper["questions"][question_type][1:]))
                # 建立sql并查询
                query = f"select question, difficultyLevel, answer from homework_or_exam_pool where hepID in {pl} ORDER BY FIELD({'hepID, ' + pl[1:-1]})"
            else:
                pl = str(tuple(store_paper["questions"][question_type][1:])[0])
                query = f"select question, difficultyLevel, answer from homework_or_exam_pool where hepID = {pl} ORDER BY FIELD({'hepID, ' + pl})"
            result = self.execute_query(query)
            # 处理结果
            if store_paper["questions"][question_type][0] > 0:
                questions_list.append("## " + question_type + f"  (一共{len(store_paper['questions'][question_type])-1}小题，每题{store_paper['questions'][question_type][0]}分，共{store_paper['questions'][question_type][0]*(len(store_paper['questions'][question_type])-1)}分)")
                if len(store_paper["score"]) < len(store_paper["questions"].keys()):
                    store_paper["score"].append(store_paper['questions'][question_type][0]*(len(store_paper['questions'][question_type])-1))
                for q_json in result:
                    answer_list.append(json.loads(q_json[2]))
                    diff_list.append(q_json[1])
                    questions_list.append(json.loads(q_json[0]))
            else:
                insert_index = len(questions_list)
                s = 0
                for q_json in result:
                    q_dict = json.loads(q_json[0])
                    q_dict["main_content"] += f"  ({sum(q_dict['score'])}分)"
                    questions_list.append(q_dict)
                    answer_list.append(json.loads(q_json[2]))
                    diff_list.append(q_json[1])
                    s += sum(q_dict["score"])
                questions_list.insert(insert_index, "## " + question_type + f"  (一共{len(result)}小题，共{s}分)")
                if len(store_paper["score"]) < len(store_paper["questions"].keys()):
                    store_paper["score"].append(s)
        result_dict = dict()
        result_dict["type"] = store_paper["type"]
        result_dict["score"] = store_paper["score"]
        result_dict["shuffle"] = store_paper["shuffle"]
        result_dict["question"] = questions_list
        result_dict["main_content"] = f"# <center>{store_paper['main_content']}</center>\n"
        return [result_dict, answer_list, diff_list, questions_list]

    def get_type_analysis(self):
        query = f"SELECT question FROM {self.table_name}"
        result = self.execute_query(query)
        type_list = []
        for q in result:
            data = json.loads(q[0])
            type_list.append(data["type"])
        type_counts = {}
        for type in type_list:
            type_counts[type] = type_counts.get(type,0)+1
        result_list = list(type_counts.items())
        pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        pie.add(
            series_name='题目类型',
            data_pair=result_list,
            rosetype='radius',
            radius='70%',
        )
        pie.set_global_opts(
            title_opts=opts.TitleOpts(title="题库中题目类型分布")
        )
        pie.set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger='item', formatter='{a} <br/>{b}:{c} ({d}%)')
        )
        html_string = pie.render_embed()
        return html_string