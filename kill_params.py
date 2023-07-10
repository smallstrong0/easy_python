#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2022/9/15 10:44 上午
# @File: kill_params.py
'''
根据表字段 快速生成各个层 需要用到的代码 按需取即可
'''
# todo 替换表名
MODEL = 'DriverDemandView'
# todo 替换表内字段
STR = ''' 
    shipper_id = Column(BigInteger, default=0, index=True, comment='shipper_id')
    driver_demand_id = Column(BigInteger, default=0, index=True, comment='driver_demand_id')
    last_ts = Column(BigInteger, default=0, index=True, comment='最后一次阅览时间戳')
    view_num = Column(Integer, default=0, comment='浏览次数')
    view_ts_list = Column(String(2048), default='[]', comment='阅览时间戳列表')
'''


def go():
    doc_list = []
    p_list = []
    d_list = []
    k_list = []
    u_list = []
    sql_params_list = []
    sql_filters_list = []
    for info in STR.split('\n'):
        if not info:
            continue
        info = info.replace('"', "'")
        name = str(info.split('=')[0]).strip()
        _type = 'String'
        if 'Integer' in info:
            _type = 'Int'
        else:
            _type = 'String'
        if 'comment' in info:
            comment = str(info.split('comment=')[1].split("\'")[1]).strip()
        else:
            comment = ''
        p = '@apiParam {' + _type + '}' + ' {} {}'.format(name, comment)
        doc_list.append(p)
        p_list.append("'{}'".format(name) + ': None,')
        if _type == 'Int':
            d_list.append("{} = int(params['{}'])".format(name, name))
        else:
            d_list.append("{} = str(params['{}'])".format(name, name))
        k_list.append("{} = {},".format(name, name))
        u_list.append("'{}' : {},".format(name, name))
        sql_params_list.append("{} = -1,".format(name))
        sql_filters_list.append("if {} != -1:\n\tfilters.append({}.{} == {})".format(name, MODEL, name, name))
    for info in doc_list:
        print(info)
    print('\n')
    for info in p_list:
        print(info)
    print('\n')
    for info in d_list:
        print(info)
    print('\n')
    for info in k_list:
        print(info)
    print('\n')
    for info in u_list:
        print(info)
    print('\n')
    for info in sql_params_list:
        print(info)
    print('\n')
    for info in sql_filters_list:
        print(info)


if __name__ == '__main__':
    go()
