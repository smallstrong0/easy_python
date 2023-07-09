#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/9/11 10:28 上午
# @File: base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, SmallInteger, Float, Boolean, DECIMAL, Text, DateTime, Date, \
    Index, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal


class Base(declarative_base()):
    __abstract__ = True

    def to_dict(self):
        return_dict = {}
        for key in self.__dict__:
            if key.startswith('_'):
                continue
            if isinstance(getattr(self, key), Decimal):
                return_dict[key] = str(getattr(self, key))
            else:
                return_dict[key] = getattr(self, key)
        return return_dict


class BaseModel(Base):
    __abstract__ = True
    ctime = Column(Integer, nullable=False, comment='创建时间')
    mtime = Column(Integer, nullable=False, comment='修改时间')
    create_by = Column(BigInteger, nullable=False, default=0, comment='创建人')
    update_by = Column(BigInteger, nullable=False, default=0, comment='更新人')
    is_delete = Column(Integer, default=0, comment='1 已经删除 0 未删除')
