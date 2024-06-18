import os

from pyecharts.charts import WordCloud
from pyecharts.options import TextStyleOpts, ToolboxOpts, InitOpts, TitleOpts

from ..orm.HepAndKpMediater import HepAndKpMediater
from .base_dao import BaseDAO



class HepAndKpMediaterDAO(BaseDAO):
    def __init__(self, db_util):
        super().__init__(db_util, HepAndKpMediater, "hep_and_kp_mediater", "mediaterID")

    def get_knowledgepoints_analysis(self):
        '''
        所有知识点的词云
        :return:
        '''
        try:
            query = f"SELECT kpName FROM {self.table_name}"
            result = self.execute_query(query)
            kpName_list = []
            for q in result:
                kpName_list.append(q[0])
            kpName_counts = {}
            for kp in kpName_list:
                kpName_counts[kp] = kpName_counts.get(kp, 0) + 1
            result_list = list(kpName_counts.items())
            wc = WordCloud(
                init_opts=InitOpts(
                    width="800px",
                    height="400px",
                    bg_color="#F0F0F0"
                )
            )
            # 设置全局选项
            wc.set_global_opts(
                title_opts=TitleOpts(
                    title="知识点词云",
                    title_textstyle_opts=dict(
                        font_size=16,
                        color="#333"
                    )
                ),
            )
            # 添加数据并渲染
            wc.add("", result_list, word_size_range=[20, 100])
            string_html = wc.render_embed()
            return string_html
        except Exception as e:
            print(e)
            return 'error'
