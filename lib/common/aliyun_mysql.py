#! /usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import contextmanager
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.model.model import *
from setting import MYSQL
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from lib.common.func import session_context_manage
import logging, functools, datetime


class cli:
    '''
    mysql数据库连接封装
    '''

    def __init__(self):
        # self.engine = create_engine(MYSQL, encoding='utf-8', pool_size=50, pool_recycle=3600, echo=True,
        #                             echo_pool=True)
        self.engine = create_engine(MYSQL, encoding='utf-8', pool_size=50, pool_recycle=3600)
        self.DBSession = sessionmaker(bind=self.engine)
        # self.DBSession = scoped_session(sessionmaker(bind=self.engine))  # 一个线程内只有一个session

    def session_maker(self, session=None):
        code = 0
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            code = -1
        finally:
            session.close()
        return code

    def create_partial_session(self):
        '''
        创建单独局部的session
        '''
        session = self.DBSession()
        return session

    def create_session(self):
        session = self.DBSession()
        session_context_manage.set(session)
        return session

    def get_session(self):
        try:
            session = session_context_manage.get()
        except Exception as e:
            session = self.create_session()
            session_context_manage.set(session)
        return session

    def finish(self):
        """
        最终提交
        """
        session = self.get_session()
        code = 0
        try:
            session.commit()
        except Exception as e:
            logging.info('{}-{}'.format('*****mysql_error*****', e))
            session.rollback()
            code = -1
        finally:
            session.close()
        return code

    def add(self, data_obj):
        """
        单条插入
        :param data_obj:
        :return:
        """
        session = self.get_session()
        try:
            session.begin(subtransactions=True)
            session.add(data_obj)
            session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}'.format('*****mysql_error*****', e))
            session.rollback()
            return -1
        finally:
            if not session:
                session.close()

    def bulk_insert(self, table, data_list):
        """
        session兼容老代码 可以不传
        批量插入 传[{}]类型
        :param table:
        :param data_list:
        :return:
        """
        session = self.get_session()
        try:
            session.begin(subtransactions=True)
            session.bulk_insert_mappings(table, data_list)
            session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, data_list))
            session.rollback()
            return -1
        finally:
            if not session:
                session.close()

    def update(self, table, filters, data_dict):
        """
        修改
        :param table:
        :param filters:
        :param data_dict:
        :return:
        """
        session = self.get_session()
        try:
            session.begin(subtransactions=True)
            session.query(table).filter(*filters).update(data_dict, synchronize_session=False)
            session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, data_dict))
            session.rollback()
            return -1
        finally:
            if not session:
                session.close()

    def delete(self, table, filters):
        """
        删除
        :param table:
        :param filters:
        :return:
        """
        session = self.get_session()
        try:
            session.begin(subtransactions=True)
            session.query(table).filter(*filters).delete(synchronize_session=False)
            session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}'.format('*****mysql_error*****', e))
            session.rollback()
            return -1
        finally:
            if not session:
                session.close()

    def bulk_update(self, table, data_list):
        """
        批量修改 传[{primary_key}]类型,根据主键确定行
        :param table:
        :param data_list:
        :return:
        """
        session = self.get_session()
        try:
            session.begin(subtransactions=True)
            session.bulk_update_mappings(table, data_list)
            session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, data_list))
            session.rollback()
            return -1
        finally:
            if not session:
                session.close()

    def find_one(self, query_list=[], join=[], join_two=[], join_three=[], filters=[], group_by=[], order_by=[]):
        """
        query_list 有五种入参及返回格式 1.[obj] 2.[obj1,obj2] 3.[obj1,field] 4.[field] 5.[field,field]
        return 对应格式 1.{} 2.[{},{}] 3. [{},1] 4. 1  5.[1,2]
        """
        obj_list_index = []
        if len(query_list) == 1 and isinstance(query_list[0], DeclarativeMeta):
            _type = 1
        else:
            _type = 2
            for i in range(len(query_list)):
                data = query_list[i]
                if isinstance(data, DeclarativeMeta):
                    # 查对象
                    obj_list_index.append(True)
                else:
                    obj_list_index.append(False)
        session = self.get_session()
        query = session.query(*query_list)
        if join:
            query = query.join(*join)
        if join_two:
            query = query.join(*join_two)
        if join_three:
            query = query.join(*join_three)
        if filters:
            query = query.filter(*filters)
        if group_by:
            query = query.group_by(*group_by)
        if order_by:
            query = query.order_by(*order_by)
        ret_data = query.first()
        if not ret_data:
            return {}
        if _type == 1:
            return ret_data.to_dict()
        else:
            _list = []
            if len(ret_data) == 1:
                return ret_data[0]
            for i in range(len(ret_data)):
                data = ret_data[i]
                if obj_list_index[i]:
                    if data:
                        _list.append(data.to_dict())
                    else:
                        _list.append(data)
                else:
                    _list.append(data)
            return _list

    def subquery(self, query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[]):
        session = self.get_session()
        query = session.query(*query_list)
        if join:
            query = query.join(*join)
        if join_two:
            query = query.join(*join_two)
        if join_three:
            query = query.join(*join_three)
        if outerjoin:
            query = query.outerjoin(*outerjoin)
        if filters:
            query = query.filter(*filters)
        return query.subquery()

    def find_list(self, query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
                  order_by=[],
                  limit=0, offset=0):
        """
        连表只允许最多三级
        :param query_list:
        :param join:
        :param join_two:
        :param join_three:
        :param outerjoin:
        :param filters:
        :param order_by:
        :param limit:
        :param offset:
        :return:
        query_list 有五种入参及返回格式 1.[obj] 2.[obj1,obj2] 3.[obj1,field] 4.[field] 5.[field,field]
        return 对应格式 1.[{}] 2.[[{},{}]] 3. [[{},1]] 4.[1] 5.[[1,2]]
        """
        session = self.get_session()
        obj_list_index = []
        if len(query_list) == 1 and isinstance(query_list[0], DeclarativeMeta):
            _type = 1
        else:
            _type = 2
            for i in range(len(query_list)):
                data = query_list[i]
                if isinstance(data, DeclarativeMeta):
                    # 查对象
                    obj_list_index.append(True)
                else:
                    obj_list_index.append(False)
        query = session.query(*query_list)
        if join:
            query = query.join(*join)
        if join_two:
            query = query.join(*join_two)
        if join_three:
            query = query.join(*join_three)
        if outerjoin:
            query = query.outerjoin(*outerjoin)
        if filters:
            query = query.filter(*filters)
        if group_by:
            query = query.group_by(*group_by)
        if order_by:
            query = query.order_by(*order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if _type == 1:
            return [obj.to_dict() for obj in query.all()]
        else:
            all_data_list = query.all()
            return_data_list = []
            for _tuple in all_data_list:
                if len(_tuple) == 1:
                    return_data_list.append(_tuple[0])
                else:
                    _list = []
                    for i in range(len(_tuple)):
                        data = _tuple[i]
                        if obj_list_index[i]:
                            if data:
                                _list.append(data.to_dict())
                            else:
                                _list.append(data)
                        else:
                            _list.append(data)
                    return_data_list.append(_list)
            return return_data_list

    def count(self, query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
              order_by=[]):
        session = self.get_session()
        query = session.query(*query_list)
        if join:
            query = query.join(*join)
        if join_two:
            query = query.join(*join_two)
        if join_three:
            query = query.join(*join_three)
        if outerjoin:
            query = query.outerjoin(*outerjoin)
        if filters:
            query = query.filter(*filters)
        if group_by:
            query = query.group_by(*group_by)
        if order_by:
            query = query.order_by(*order_by)
        ret_data = query.scalar()
        return ret_data or 0

    def rollback(self):
        self.get_session().rollback()

    def close(self):
        self.get_session().close()

    def commit(self):
        self.get_session().commit()

    def sql_execute(self, sql_str):
        session = self.get_session()
        try:
            return session.execute(sql_str)
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, sql_str))
            session.rollback()
            return None
        finally:
            if not session:
                session.close()


mysql_rds = cli()


@contextmanager
def session_context():
    session = mysql_rds.create_partial_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if session:
            session.close()
