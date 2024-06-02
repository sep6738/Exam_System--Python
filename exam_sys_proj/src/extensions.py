# 为了解决循环引用的问题

# src-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from ..util.db_util import DBUtil
try:
    dbPool = DBUtil('./util/config.yaml')
except Exception as e:
    dbPool = DBUtil('exam_sys_proj/util/config.yaml')
db = SQLAlchemy()
mail = Mail()
