#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Put your models here

from sqlalchemy import Column, BigInteger, Integer, String, SmallInteger, Float, Boolean, DECIMAL, Text, DateTime, Date, \
    Index, UniqueConstraint
from sqlalchemy.dialects.mysql import MEDIUMTEXT, LONGTEXT, BIGINT, INTEGER, SMALLINT, TINYINT, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal
from sqlalchemy.schema import Sequence
from lib.model.base import Base, BaseModel

""" 
建表规范
1.之后建表 请继承BaseModel
2.表字段主键自增强制取名 不允许是id
3.comment备注强制每个字段都要
4.建表之后如果如果关联其他表字段时候 名字别乱取 要统一
5.字段取名 出现下划线警示时候请自行注意单词拼写
"""


class ApiLog(Base):
    __tablename__ = "api_log"
    __doc__ = '接口log'
    log_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='日志主键')
    ctime = Column(Integer, nullable=False, comment='创建时间')
    date_time_in = Column(String(30), nullable=False, default='', comment='调用时间')
    date_time_out = Column(String(30), nullable=False, default='', comment='返回时间')
    time_consuming = Column(Integer, nullable=False, default=0, comment='接口耗时 单位毫秒')

    url_index = Column(String(256), nullable=False, default='', index=True, comment='url index')
    method = Column(String(10), nullable=False, default='', comment='http method')

    url = Column(String(1024), nullable=False, default='', comment='http path url')
    params = Column(String(1024), nullable=False, default='{}', comment='url参数')
    body = Column(Text, nullable=False, default='{}', comment='body参数')
    response = Column(Text, nullable=False, default='{}', comment='返回结果')

    user_id = Column(BigInteger, nullable=False, index=True, comment='登录用户的user_id')
    result = Column(String(10), nullable=False, default='SUCCESS', comment='结果')


class Test(BaseModel):
    __tablename__ = 'test'
    test_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    test_name = Column(String(128), nullable=False, default="")


class Goods(BaseModel):
    __tablename__ = 'goods'
    goods_id = Column(INTEGER(11), primary_key=True, autoincrement=True)
    goods_name = Column(String(128), nullable=False, default="")

if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session
    from sqlalchemy import create_engine
    from setting import MYSQL

    engine = create_engine(MYSQL)
    DBSession = scoped_session(sessionmaker(bind=engine))

    Base.metadata.create_all(engine)
