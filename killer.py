#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/11 3:19 下午
# @File: killer.py

import configparser
from string import Template
import time
import os

config = configparser.ConfigParser()
config.read("killer.ini")
SETTING_DIC = {}
for i in config.items():
    key = i[0]
    dic = {}
    for k in i[1].items():
        dic[k[0]] = k[1]
    SETTING_DIC[key] = dic
print(SETTING_DIC)


def str_hump(text):
    text = text.capitalize()
    arr = filter(None, text.split('_'))
    res = ''
    j = 0
    for i in arr:
        if j == 0:
            res = i
        else:
            res = res + i[0].upper() + i[1:]
        j += 1
    return res


CREATE_TIME = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
table = SETTING_DIC['CORE']['table']
TABLE = table.upper()
Table = str_hump(table)
CREATE_BY = SETTING_DIC['CORE']['create_by']
VIEW_PATH = SETTING_DIC['VIEW']['path']
VIEW_MODULE = SETTING_DIC['VIEW']['module']
DAP_PATH = SETTING_DIC['DAP']['path']
DAO_PATH = SETTING_DIC['DAO']['path']
REDIS_KEY_PATH = SETTING_DIC['DAO']['redis_key_path']
TEST_PATH = SETTING_DIC['TEST']['path']
TEST_MODULE = SETTING_DIC['TEST']['module']
ERROR_PATH = SETTING_DIC['ERROR']['path']
CODE_START = int(SETTING_DIC['ERROR']['code_start'])
TABLE_NAME = str(SETTING_DIC['ERROR']['table_name'])
VERSION = str(SETTING_DIC['API']['version'])
MODULE = str(SETTING_DIC['API']['module'])
FUNCTION = str(SETTING_DIC['API']['func'])
VIEW_URL_PATH = str(SETTING_DIC['API']['url_path'])
IMPORT_POS = int(SETTING_DIC['API']['url_import_pos'])
ROUTE_POS = int(SETTING_DIC['API']['url_route_pos'])
CREATE_MODE = str(SETTING_DIC['CREATE_MODE']['module'])


# Template使用参考 https://www.cnblogs.com/subic/p/6552752.html
def writer_master(template_path, output_path, data_dic):
    lines = []
    class_file = open(output_path, "wt")
    template_file = open(template_path, 'r')
    lines.append(Template(template_file.read()).safe_substitute(data_dic))
    class_file.writelines(lines)
    class_file.close()


def create_view():
    if not os.path.exists('{}{}'.format(VIEW_PATH, VIEW_MODULE)):
        os.makedirs('{}{}'.format(VIEW_PATH, VIEW_MODULE))
    writer_master(
        template_path='./template/view',
        output_path='{}{}/{}.py'.format(VIEW_PATH, VIEW_MODULE, table),
        data_dic={
            'CREATE_BY': CREATE_BY,
            'CREATE_TIME': CREATE_TIME,
            'table': table,
            'TABLE': TABLE,
            'Table': Table,
            'version': VERSION,
            'module': MODULE,
            'func': FUNCTION,
        }
    )
    if not os.path.exists('{}{}/__init__.py'.format(VIEW_PATH, VIEW_MODULE)):
        writer_master(
            template_path='./template/view_init',
            output_path='{}{}/__init__.py'.format(VIEW_PATH, VIEW_MODULE),
            data_dic={
                'CREATE_BY': CREATE_BY,
                'CREATE_TIME': CREATE_TIME,
                'table': table,
                'TABLE': TABLE,
                'Table': Table,
            }
        )
        view_import = True
    else:
        with open('{}{}/__init__.py'.format(VIEW_PATH, VIEW_MODULE), encoding="utf-8", mode="a") as file:
            file.write('\nfrom .{} import *'.format(table))
            view_import = False



def create_test():
    if not os.path.exists('{}{}'.format(TEST_PATH, TEST_MODULE)):
        os.makedirs('{}{}'.format(TEST_PATH, TEST_MODULE))
    writer_master(
        template_path='./template/test',
        output_path='{}{}/test_{}.py'.format(TEST_PATH, TEST_MODULE, table),
        data_dic={
            'CREATE_BY': CREATE_BY,
            'CREATE_TIME': CREATE_TIME,
            'table': table,
            'TABLE': TABLE,
            'Table': Table,
            'module': MODULE,
            'func': FUNCTION,
        }
    )
    if not os.path.exists('{}{}/__init__.py'.format(TEST_PATH, TEST_MODULE)):
        writer_master(
            template_path='./template/test_init',
            output_path='{}{}/__init__.py'.format(TEST_PATH, TEST_MODULE),
            data_dic={
                'CREATE_BY': CREATE_BY,
                'CREATE_TIME': CREATE_TIME,
            }
        )

def create_dap():
    writer_master(
        template_path='./template/dap',
        output_path='{}{}.py'.format(DAP_PATH, table),
        data_dic={
            'CREATE_BY': CREATE_BY,
            'CREATE_TIME': CREATE_TIME,
            'table': table,
            'TABLE': TABLE,
            'Table': Table,
        }
    )


def create_dao():
    writer_master(
        template_path='./template/dao',
        output_path='{}{}.py'.format(DAO_PATH, table),
        data_dic={
            'CREATE_BY': CREATE_BY,
            'CREATE_TIME': CREATE_TIME,
            'table': table,
            'TABLE': TABLE,
            'Table': Table,
        }
    )

    writer_master(
        template_path='./template/dao_mysql',
        output_path='{}{}_mysql.py'.format(DAO_PATH, table),
        data_dic={
            'CREATE_BY': CREATE_BY,
            'CREATE_TIME': CREATE_TIME,
            'table': table,
            'TABLE': TABLE,
            'Table': Table,
        }
    )

    writer_master(
        template_path='./template/dao_redis',
        output_path='{}{}_redis.py'.format(DAO_PATH, table),
        data_dic={
            'CREATE_BY': CREATE_BY,
            'CREATE_TIME': CREATE_TIME,
            'table': table,
            'TABLE': TABLE,
            'Table': Table,
        }
    )

    with open(REDIS_KEY_PATH, encoding="utf-8", mode="a") as file:
        file.write('\n\n' + "# {}相关".format(TABLE_NAME) + '\n')
        file.write('class {}Redis(object):'.format(Table) + '\n')
        file.write('    UNIQUE_KEY = PREFIX + "{}:"'.format(table) + "+'{}'\n")
        file.write('    EX = 86400 * 15 + random.randint(1800, 3600)\n')

    with open(ERROR_PATH, encoding="utf-8", mode="a") as file:
        file.write('\n\n' + "# {}相关".format(TABLE_NAME) + '\n')
        file.write('class {}ErrorType(Enum):'.format(Table) + '\n')
        error_list = [
            '    {}_ADD_ERROR = ({}, "{}添加失败")',
            '    {}_BULK_ADD_ERROR = ({}, "{}批量添加失败")',
            '    {}_UPDATE_ERROR = ({}, "{}修改失败")',
            '    {}_BULK_UPDATE_ERROR = ({}, "{}批量修改失败")',
            '    {}_DELETE_ERROR = ({}, "{}删除失败")'
        ]
        global CODE_START
        for txt in error_list:
            file.write(txt.format(TABLE, CODE_START, TABLE_NAME) + '\n')
            CODE_START = CODE_START + 1


if __name__ == '__main__':
    if 'view' in CREATE_MODE:
        create_view()
    if 'test' in CREATE_MODE:
        create_test()
    if 'dap' in CREATE_MODE:
        create_dap()
    if 'dao' in CREATE_MODE:
        create_dao()
