#! /usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: ss
# @Time: 2020/7/11 3:19 下午
# @File: killer.py

import configparser
from string import Template
import time
import os
import re

config = configparser.ConfigParser()
config.read("killer.ini", encoding='utf-8')
SETTING_DIC = {}
for i in config.items():
    key = i[0]
    dic = {}
    for k in i[1].items():
        dic[k[0]] = k[1]
    SETTING_DIC[key] = dic
print(SETTING_DIC)


def find_start_num():
    input_str = ''
    with open('./lib/common/error.py', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            input_str += line

    pattern = re.compile(r"\d+")
    s = pattern.finditer(input_str)
    tmp = []
    for i in s:
        tmp.append((i.group(), i.regs[0]))
    # 求出最大的数及对应下标
    max_int = max(map(int, [c[0] for c in tmp]))
    tmp = [i for i in tmp if i[0] == str(max_int)]
    find = []
    for t in tmp:
        inx = t[1][1]
        xiaoshu = ""
        _f = t[0]
        if len(input_str) != inx and input_str[inx] == ".":
            _inx = inx
            for c in range(len(input_str[inx + 1:])):
                if input_str[_inx + 1].isdigit():
                    _inx += 1
                else:
                    break
            xiaoshu = input_str[inx + 1:_inx + 1]
        if xiaoshu:
            _f = t[0] + "." + xiaoshu
        find.append(_f)
    find = max(map(float, find))
    return (int(int(find) / 100) + 1) * 100


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
VIEW_MODULE = table
DAP_PATH = SETTING_DIC['DAP']['path']
DAO_PATH = SETTING_DIC['DAO']['path']
REDIS_KEY_PATH = SETTING_DIC['DAO']['redis_key_path']
TEST_PATH = SETTING_DIC['TEST']['path']
TEST_MODULE = table
ERROR_PATH = SETTING_DIC['ERROR']['path']
TABLE_NAME = str(SETTING_DIC['CORE']['table_name'])
VERSION = str(SETTING_DIC['API']['version'])
MODULE = table
FUNCTION = str(SETTING_DIC['API']['func'])
VIEW_URL_PATH = str(SETTING_DIC['API']['url_path'])
IMPORT_POS = 2
ROUTE_POS = 0
CREATE_MODE = str(SETTING_DIC['CREATE_MODE']['mode'])
CODE_START = find_start_num()


# Template使用参考 https://www.cnblogs.com/subic/p/6552752.html
def writer_master(template_path, output_path, data_dic):
    lines = []
    class_file = open(output_path, "wt", encoding='utf-8')
    template_file = open(template_path, 'r', encoding='utf-8')
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
            'table_name': TABLE_NAME,
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
    with open(VIEW_URL_PATH, "r+", encoding="u8") as fp:
        header = ''
        body = ''
        footer = ''
        for i, d in enumerate(fp.readlines(), start=1):
            if i <= IMPORT_POS:
                header += d
            # elif IMPORT_POS < i < ROUTE_POS:
            #     body += d

            else:
                if d == ']\n':
                    pass
                else:
                    body += d

        fp.seek(0)  # 回到初始点
        fp.write(header)
        if view_import:
            fp.write("import handler.api.{} as {}".format(VIEW_MODULE, VIEW_MODULE) + "\n")
        fp.write(body)
        fp.write("    [r'/{}/{}', {}.{}Handler],".format(MODULE, FUNCTION, VIEW_MODULE, Table) + "\n")
        fp.write("    [r'/{}/{}/list', {}.{}ListHandler],".format(MODULE, FUNCTION, VIEW_MODULE, Table) + "\n")
        fp.write("]" + "\n")
        # fp.write(footer)


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
