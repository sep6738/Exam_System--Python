
class BaseDAO:
    def __init__(self, db_util, entity_class, table_name, primary_key):
        self.db_util = db_util
        self.entity_class = entity_class
        self.table_name = table_name
        self.primary_key = primary_key


    def batchInsert(self, entity_list:list, access_protected):
        try:
            entity = entity_list[0]
            columns = [attr for attr in dir(entity) if not callable(getattr(entity, attr)) and not attr.startswith("_")]
            # 获取各属性的值
            # 对代码["_"+pp for pp in columns]的解释：
            # 加入_直接取只经过set方法处理的数据，如果不要_那么取到的值会经过set方法和get方法的处理
            if access_protected:
                values = [getattr(entity, col) for col in ["_"+pp for pp in columns]]
            else:
                values = [getattr(entity, col) for col in columns]
            # 构建占位符
            placeholders = ", ".join(["%s"] * len(columns))
            # 构建sql
            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            # print(query)
            # 传sql
            new_pk = self.execute_update(query, values)
            return new_pk
        except Exception as e:
            print(e)
            return "error"
    # 插入数据，传入orm的一个实例
    def insert(self, entity, access_protected=True):
        """
        插入一条数据，传入orm的一个对象，若表的主键自增建议设置主键为None,函数会返回此次插入的数据的主键\n
        使用示例：\n
        xtable = XTable(column1 = "ab",column2 = "45")\n
        xtableDAO = XTableDAO()\n
        pk = xtableDAO.insert(xtable)\n
        数据库结果：\n
        +---------+---------+\n
        | column1 | column2 |\n
        +---------+---------+\n
        |   ab    |   45    |\n
        +---------+---------+\n
        :param entity:orm对象
        :param access_protected:是否访问私有属性，若为true则从对象取值时值仅被set方法处理，若为false则会经过set和get方法处理
        :return:新插入数据的主键->any
        """
        # 利用orm进行反射构建column列表存储表的所有属性
        try:
            columns = [attr for attr in dir(entity) if not callable(getattr(entity, attr)) and not attr.startswith("_")]
            # 获取各属性的值
            # 对代码["_"+pp for pp in columns]的解释：
            # 加入_直接取只经过set方法处理的数据，如果不要_那么取到的值会经过set方法和get方法的处理
            if access_protected:
                values = [getattr(entity, col) for col in ["_"+pp for pp in columns]]
            else:
                values = [getattr(entity, col) for col in columns]
            # 构建占位符
            placeholders = ", ".join(["%s"] * len(columns))
            # 构建sql
            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            # print(query)
            # 传sql
            new_pk = self.execute_update(query, values)
            return new_pk
        except Exception as e:
            print(e)
            return "error"

    # 根据主键查询
    def query(self, value, column_name=None, is_all=False):
        """
        根据某个属性查询，默认根据主键查询\n
        默认仅查询一行,若结果是多行则仅输出第一行\n
        可以设置is_all为true来得到存有多行结果的列表\n
        传入属性名和要查询的值\n
        示例：\n
        xtableDAO = XTableDAO()\n
        xtable = xtableDAO.query(1)\n
        查询xtable表主键为1的行，并返回一个xtable表的orm对象赋值给xtable\n
        xtable = xtableDAO.query("小明", "name")\n
        查询xtable表name为"小明"的行，并返回一个xtable表的orm对象赋值给xtable\n
        :param is_all: 是否输出全部结果默认为false
        :param value: 值
        :param column_name: 属性名
        :return: 若is_all为false则输出封装有结果的orm对象->orm；若为true则输出元素为orm对象的列表->list
        """
        if not column_name:
            column_name = self.primary_key
        try:
            columns = [attr for attr in dir(self.entity_class) if not callable(getattr(self.entity_class, attr)) and not attr.startswith("_")]
            query = f"SELECT {', '.join(columns)} FROM {self.table_name} WHERE {column_name} = %s"
            result = self.execute_query(query, (value,))
            if result:
                if is_all:
                    result_list = []
                    for i in result:
                        result_list.append(self._create_entity_from_row(i))
                    return result_list
                else:
                    return self._create_entity_from_row(result[0])
            return None
        except Exception as e:
            print(e)
            return "error"

    def update(self, entity, value, column_name=None):
        """
        根据列名更新数据库数据，默认根据主键
        接收封装过数据的orm对象，读取读取对象内部的数据，并存到数据库中\n
        示例：\n
        原数据表：\n
        +---------+---------+\n
        | column1 | column2 |\n
        +---------+---------+\n
        |   cd    |   88    |\n
        +---------+---------+\n
        xtable = XTable(column1 = "ab",column2 = "45")\n
        xtableDAO = XTableDAO()\n
        xtable = xtableDAO.update(xtable, "cd", "column1")\n
        #将xtable表中column1为cd的列更新\n
        结果：\n
        +---------+---------+\n
        |   ab    |   45    |\n
        +---------+---------+\n
        如果第一步设置：\n
        xtable = XTable(column1 = "ab",column2 = "")\n
        结果（将column2置空）：\n
        +---------+---------+\n
        |   ab    |         |\n
        +---------+---------+\n
        如果第一步设置：\n
        xtable = XTable(column1 = "ab",column2 = None)\n
        结果（不修改column2）：\n
        +---------+---------+\n
        |   ab    |    88   |\n
        +---------+---------+\n
        :param value: 要更新列的值
        :param column_name:要根据的列名默认为None，None值时根据主键更新
        :param entity:对应的orm对象
        :return:成功为True失败为False->bool
        """
        if not column_name:
            column_name = self.primary_key
        try:
            columns = [attr for attr in dir(self.entity_class) if not callable(getattr(self.entity_class, attr)) and not attr.startswith("_")]
            values = [getattr(entity, col) for col in ["_"+pp for pp in columns]]

            excludeAndSetNone_index = []
            for i in range(len(values)):
                if values[i] is None:
                    excludeAndSetNone_index.append(i)
                elif values[i] == "":
                    excludeAndSetNone_index.append(str(i))
            n = 0
            for i in excludeAndSetNone_index:
                if isinstance(i, str):
                    values[eval(i) - n] = None
                else:
                    columns.pop(i - n)
                    values.pop(i - n)
                n += 1

            set_clause = ", ".join([f"{col} = %s" for col in columns])
            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {column_name} = %s"
            values.append(value)
            self.execute_update(query, values)
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, value, column_name=None):
        """
        根据列名和值删除数据库数据，默认根据主键
        若列名输为None则使用默认即更具主键删除
        :param column_name: 根据的列的名称->str
        :param value:
        :return:成功为True失败为False->bool
        """
        if not column_name:
            column_name = self.primary_key
        try:
            query = f"DELETE FROM {self.table_name} WHERE {column_name} = %s"
            self.execute_update(query, (value,))
            return True
        except Exception as e:
            print(e)
            return False

    def execute_query(self, query, params=None):
        conn = self.db_util.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def execute_update(self, query, params=None):
        conn = self.db_util.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                new_pk = cursor.lastrowid
                return new_pk
        finally:
            conn.close()

    def _create_entity_from_row(self, row):
        entity = self.entity_class()
        for attr, value in zip([attr for attr in dir(entity) if not callable(getattr(entity, attr)) and not attr.startswith("_")], row):
            setattr(entity, attr, value)
        return entity
