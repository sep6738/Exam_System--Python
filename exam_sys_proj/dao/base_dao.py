
class BaseDAO:
    def __init__(self, db_util, entity_class, table_name, primary_key):
        self.db_util = db_util
        self.entity_class = entity_class
        self.table_name = table_name
        self.primary_key = primary_key

    # 插入数据，传入orm的一个实例
    def insert(self, entity):
        """
        插入数据，传入orm的一个对象，若表的主键自增建议设置主键为None,函数会返回此次插入的数据的主键
        :param entity:
        :return:new_pk
        """
        # 利用orm进行反射构建column列表存储表的所有属性
        columns = [attr for attr in dir(entity) if not callable(getattr(entity, attr)) and not attr.startswith("_")]
        # 获取各属性的值
        # 对代码["_"+pp for pp in columns]的解释：
        # 加入_直接取只经过set方法处理的数据，如果不要_那么取到的值会经过set方法和get方法的处理
        values = [getattr(entity, col) for col in ["_"+pp for pp in columns]]
        # 构建占位符
        placeholders = ", ".join(["%s"] * len(columns))
        # 构建sql
        query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
        # print(query)
        # 传sql
        new_pk = self._execute_update(query, values)
        return new_pk

    # 根据主键查询
    def query(self, entity, primary_key_value):
        """
        根据主键查询
        :param entity:
        :param primary_key_value:
        :return:
        """
        columns = [attr for attr in dir(entity) if not callable(getattr(entity, attr)) and not attr.startswith("_")]
        query = f"SELECT {', '.join(columns)} FROM {self.table_name} WHERE {self.primary_key} = %s"
        result = self._execute_query(query, (primary_key_value,))
        if result:
            return self._create_entity_from_row(result[0])
        return None

    def update(self, entity):
        """
        根据主键更新数据库一行数据
        :param entity:
        :return:
        """
        columns = [attr for attr in dir(entity) if not callable(getattr(entity, attr)) and not attr.startswith("_")]
        values = [getattr(entity, col) for col in ["_"+pp for pp in columns]]
        set_clause = ", ".join([f"{col} = %s" for col in columns])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {self.primary_key} = %s"
        values.append(getattr(entity, self.primary_key))
        self._execute_update(query, values)

    def delete(self, primary_key_value):
        """
        根据主键删除数据库一行数据
        :param primary_key_value:
        :return:
        """
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = %s"
        self._execute_update(query, (primary_key_value,))

    def _execute_query(self, query, params=None):
        conn = self.db_util.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def _execute_update(self, query, params=None):
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
