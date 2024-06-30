from dbutils.pooled_db import PooledDB
import pymysql
from .config import Config
import threading


class DBUtil:
    _instance_lock = threading.Lock()
    _pool = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(DBUtil, "_instance"):
            with DBUtil._instance_lock:
                if not hasattr(DBUtil, "_instance"):
                    DBUtil._instance = super().__new__(cls)
                    cls._initialize_pool(cls, *args, **kwargs)
        return DBUtil._instance

    def _initialize_pool(cls, config_file='config.yaml'):
        config = Config(config_file).get_database_config()
        cls._pool = PooledDB(
            creator=pymysql,
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            mincached=config['mincached'],
            maxcached=config['maxcached'],
            blocking=True,  # 在达到最大连接数时阻塞等待
            maxusage=None,  # 连接使用的最大次数
            setsession=[],  # 会话初始化命令
            ping=1
        )

    def get_connection(self):
        return self._pool.connection()
