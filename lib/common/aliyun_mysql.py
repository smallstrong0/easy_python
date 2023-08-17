#! /usr/bin/env python
# -*- coding: utf-8 -*-
from setting import MYSQL
from sqlalchemy.orm.decl_api import DeclarativeMeta
from lib.common.func import session_context_manage
import logging, functools, datetime
from sqlalchemy import or_, and_, any_, text, exists, func, distinct, between, case, select, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncAttrs


class cli:
    '''
    mysql数据库连接封装
    '''

    def __init__(self):
        self.async_engine = create_async_engine(MYSQL, pool_size=50, pool_recycle=3600, echo=True)
        # 创建异步数据库会话
        self.DBSession = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession
        )

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

    async def finish(self, session=None):
        """
        最终提交
        """
        if not session:
            session = self.get_session()
        code = 0
        try:
            await session.commit()
        except Exception as e:
            logging.info('{}-{}'.format('*****mysql_error*****', e))
            await session.rollback()
            code = -1
        finally:
            await session.close()
        return code

    async def add(self, data_obj):
        """
        单条插入
        :param data_obj:
        :return:
        """
        session = self.get_session()
        try:
            session.begin_nested()
            session.add(data_obj)
            await session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}'.format('*****mysql_error*****', e))
            await session.rollback()
            return -1
        finally:
            if not session:
                await session.close()

    async def bulk_insert(self, data_list):
        """
        批量插入 传[{}]类型
        :param table:
        :param data_list:
        :return:
        """
        session = self.get_session()
        try:
            session.begin_nested()
            session.add_all(data_list)
            await session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, data_list))
            await session.rollback()
            return -1
        finally:
            if not session:
                await session.close()

    async def update(self, table, filters, data_dict):
        """
        修改
        :param table:
        :param filters:
        :param data_dict:
        :return:
        """
        session = self.get_session()
        try:
            session.begin_nested()
            await session.execute(update(table).where(*filters).values(data_dict))
            await session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, data_dict))
            await session.rollback()
            return -1
        finally:
            if not session:
                await session.close()

    async def delete(self, table, filters):
        """
        删除
        :param table:
        :param filters:
        :return:
        """
        session = self.get_session()
        try:
            session.begin_nested()
            await session.execute(delete(table).where(*filters))
            await session.commit()
            return 0
        except Exception as e:
            logging.info('{}-{}'.format('*****mysql_error*****', e))
            await session.rollback()
            return -1
        finally:
            if not session:
                await session.close()

    # async def bulk_update(self, table, data_list):
    #     """
    #     批量修改 传[{primary_key}]类型,根据主键确定行
    #     :param table:
    #     :param data_list:
    #     :return:
    #     """
    #     session = self.get_session()
    #     try:
    #         session.begin_nested()
    #         await session.bulk_update_mappings(table, data_list) # todo error
    #         await session.commit()
    #         return 0
    #     except Exception as e:
    #         logging.info('{}-{}-{}'.format('*****mysql_error*****', e, data_list))
    #         await session.rollback()
    #         return -1
    #     finally:
    #         if not session:
    #             await session.close()

    async def find_one(self, query_list=[], join=[], join_two=[], join_three=[], filters=[], group_by=[], order_by=[]):
        """
        query_list 有五种入参及返回格式 1.[obj] 2.[obj1,obj2] 3.[obj1,field] 4.[field] 5.[field,field]
        return 对应格式 1.{} 2.[{},{}] 3. [{},1] 4. 1  5.[1,2]
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
        query = select(*query_list)
        if join:
            query = query.join(*join)
        if join_two:
            query = query.join(*join_two)
        if join_three:
            query = query.join(*join_three)
        if filters:
            query = query.where(*filters)
        if group_by:
            query = query.group_by(*group_by)
        if order_by:
            query = query.order_by(*order_by)
        res = await session.execute(query)
        ret_data = res.fetchone()
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

    # def subquery(self, query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[]):
    #     session = self.get_session() # todo
    #     query = select(*query_list)
    #     if join:
    #         query = query.join(*join)
    #     if join_two:
    #         query = query.join(*join_two)
    #     if join_three:
    #         query = query.join(*join_three)
    #     if outerjoin:
    #         query = query.outerjoin(*outerjoin)
    #     if filters:
    #         query = query.where(*filters)
    #     return query.subquery()

    async def find_list(self, query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
                        having=[],
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
        query = select(*query_list)
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
            if having:
                query.having(*having)
        if order_by:
            query = query.order_by(*order_by)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        res = await session.execute(query)
        ret_data = res.fetchall()

        if _type == 1:
            return [obj[0].to_dict() for obj in ret_data]
        else:
            return_data_list = []
            for _tuple in ret_data:
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

    async def count(self, query_list=[], join=[], join_two=[], join_three=[], outerjoin=[], filters=[], group_by=[],
                    having=[],
                    order_by=[]):
        session = self.get_session()
        query = select(*query_list)
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
            if having:
                query.having(*having)
        if order_by:
            query = query.order_by(*order_by)
        count = await session.execute(query)
        return count.scalar() or 0

    async def rollback(self):
        await self.get_session().rollback()

    async def close(self):
        await self.get_session().close()

    async def commit(self):
        await self.get_session().commit()

    async def sql_execute(self, sql_str):
        session = self.get_session()
        try:
            return await session.execute(sql_str)
        except Exception as e:
            logging.info('{}-{}-{}'.format('*****mysql_error*****', e, sql_str))
            await session.rollback()
            return None
        finally:
            if not session:
                await session.close()


mysql_rds = cli()
