# ! /usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from tornado.web import HTTPError

status_0 = dict(status_code=405, reason='Method not allowed.')
status_1 = dict(status_code=404, reason='API not found.')


class CommonError(HTTPError):
    def __init__(self, error):
        if isinstance(error, tuple) and len(error) == 2:
            pass
        else:
            raise Exception('error must tuple and length is two')
        super(CommonError, self).__init__(
            200
        )
        self.common_error = error


class CommonErrorType(Enum):
    UNEXCEPT_ERROR = (-1, '未知异常，请联系客服')
    INVALID_SIG = (-3, '登陆超时，请重新登陆')
    TOKEN_NULL = (-2, 'cannot get user\'s token')
    INVALID_ROLE = (-5, '无效角色身份')
    INVALID_REGION = (-6, '无效的地区名')
    CREATE_ID_ERROR = (-7, '生成id失败')
    NO_RIGHT_ACCESS = (-8, '无操作权限')
    PARAMS_ERROR = (-9, '参数错误')
    WX_ACCESS_TOKEN_ERROR = (-10, '获取微信access_token失败')
    DATA_ERROR = (-11, '数据提交失败')


# 示例相关
class DemoErrorType(Enum):
    DEMO_ADD_ERROR = (34300, "示例添加失败")
    DEMO_BULK_ADD_ERROR = (34301, "示例批量添加失败")
    DEMO_UPDATE_ERROR = (34302, "示例修改失败")
    DEMO_BULK_UPDATE_ERROR = (34303, "示例批量修改失败")
    DEMO_DELETE_ERROR = (34304, "示例删除失败")


# 测试相关
class TestErrorType(Enum):
    TEST_ADD_ERROR = (100, "测试添加失败")
    TEST_BULK_ADD_ERROR = (101, "测试批量添加失败")
    TEST_UPDATE_ERROR = (102, "测试修改失败")
    TEST_BULK_UPDATE_ERROR = (103, "测试批量修改失败")
    TEST_DELETE_ERROR = (104, "测试删除失败")


# 测试相关
class TestErrorType(Enum):
    TEST_ADD_ERROR = (34400, "测试添加失败")
    TEST_BULK_ADD_ERROR = (34401, "测试批量添加失败")
    TEST_UPDATE_ERROR = (34402, "测试修改失败")
    TEST_BULK_UPDATE_ERROR = (34403, "测试批量修改失败")
    TEST_DELETE_ERROR = (34404, "测试删除失败")
