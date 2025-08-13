# -*- coding: utf-8 -*-

import re
from datetime import datetime, date
from typing import Annotated, Optional, Union
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema

from app.common.constant import RET
from app.core.exceptions import CustomException


# 自定义日期时间字符串类型
DateTimeStr = Annotated[
    datetime,
    AfterValidator(lambda x: datetime_validator(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 自定义日期类型
DateStr = Annotated[
    date,
    AfterValidator(lambda x: date_validator(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 自定义手机号类型
Telephone = Annotated[
    str,
    AfterValidator(lambda x: mobile_validator(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 自定义邮箱类型
Email = Annotated[
    str,
    AfterValidator(lambda x: email_validator(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

def datetime_validator(value: Union[str, datetime]) -> Union[str, datetime, None]:
    """
    日期格式验证器
    
    :param value: 日期值
    :return: 格式化后的日期
    :raises: CustomException 日期格式无效时抛出
    """
    pattern = "%Y-%m-%d %H:%M:%S"
    try:
        if isinstance(value, str):
            value = datetime.strptime(value, pattern)
        elif isinstance(value, datetime):
            value = value.strftime(pattern)
    except Exception:
        raise CustomException(code=RET.BAD_REQUEST.code, msg="无效的日期格式")

    return value

def date_validator(value: Union[str, date]) -> Union[str, date, None]:
    """
    日期格式验证器
    
    :param value: 日期值
    :return: 格式化后的日期
    :raises: CustomException 日期格式无效时抛出
    """
    pattern = "%Y-%m-%d"
    try:
        if isinstance(value, str):
            value = date.fromisoformat(value)
        elif isinstance(value, date):
            value = value.strftime(pattern)
    except Exception:
        raise CustomException(code=RET.BAD_REQUEST.code, msg="无效的日期格式")

    return value


def email_validator(value: str) -> str:
    """
    邮箱地址验证器
    
    :param value: 邮箱地址
    :return: 验证后的邮箱地址
    :raises: CustomException 邮箱格式无效时抛出
    """
    if not value:
        raise CustomException(code=RET.BAD_REQUEST.code, msg="邮箱地址不能为空")

    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(regex, value):
        raise CustomException(code=RET.BAD_REQUEST.code, msg="邮箱地址格式不正确")

    return value

def mobile_validator(value: Optional[str]) -> str:
    """
    手机号验证器
    
    :param value: 手机号
    :return: 验证后的手机号
    :raises: CustomException 手机号格式无效时抛出
    """
    if not value:
        return value

    if len(value) != 11 or not value.isdigit():
        raise CustomException(code=RET.BAD_REQUEST.code, msg="手机号格式不正确")

    regex = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

    if not re.match(regex, value):
        raise CustomException(code=RET.BAD_REQUEST.code, msg="手机号格式不正确")

    return value

def menu_request_validator(data):
    """
    菜单请求数据验证器
    
    :param data: 请求数据
    :return: 验证后的请求数据
    :raises: CustomException 请求数据无效时抛出
    """
    menu_types = {1: "目录", 2: "功能", 3: "权限"}
    
    if data.type not in menu_types:
        raise CustomException(code=RET.BAD_REQUEST.code, msg=f"菜单类型必须为: {','.join(map(str, menu_types.keys()))}")
    
    if data.type in [1, 2]:
        if not data.route_name:
            raise CustomException(code=RET.BAD_REQUEST.code, msg="路由名称不能为空")
        if not data.route_path:
            raise CustomException(code=RET.BAD_REQUEST.code, msg="路由路径不能为空")
            
    if data.type == 2 and not data.component_path:
        raise CustomException(code=RET.BAD_REQUEST.code, msg="组件路径不能为空")
        
    return data

def role_permission_request_validator(data):
    """
    角色权限设置数据验证器
    
    :param data: 请求数据
    :return: 验证后的请求数据
    :raises: CustomException 请求数据无效时抛出
    """
    data_scopes = {
        1: "仅本人数据权限",
        2: "本部门数据权限", 
        3: "本部门及以下数据权限",
        4: "全部数据权限",
        5: "自定义数据权限"
    }
    
    if data.data_scope not in data_scopes:
        raise CustomException(code=RET.BAD_REQUEST.code, msg=f"数据权限范围必须为: {','.join(map(str, data_scopes.keys()))}")
        
    if not data.role_ids:
        raise CustomException(code=RET.BAD_REQUEST.code, msg="角色不能为空")
        
    return data
