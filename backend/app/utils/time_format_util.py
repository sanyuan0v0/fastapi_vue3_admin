# -*- coding: utf-8 -*-

import datetime
from typing import Any, List, Dict


class TimeFormatUtil:
    """
    时间格式化工具类
    """
    
    DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    @classmethod
    def object_format_datetime(cls, obj: Any) -> Any:
        """
        格式化对象中的datetime类型属性
        
        :param obj: 输入对象
        :return: 格式化后的对象
        """
        for attr in dir(obj):
            if not attr.startswith('_'):  # 跳过私有属性
                value = getattr(obj, attr)
                if isinstance(value, datetime.datetime):
                    setattr(obj, attr, value.strftime(cls.DEFAULT_DATETIME_FORMAT))
        return obj

    @classmethod
    def list_format_datetime(cls, lst: List[Any]) -> List[Any]:
        """
        格式化对象列表中所有对象的datetime类型属性
        
        :param lst: 对象列表
        :return: 格式化后的对象列表
        """
        return [cls.object_format_datetime(obj) for obj in lst]

    @classmethod
    def format_datetime_dict_list(cls, dicts: List[Dict]) -> List[Dict]:
        """
        递归格式化字典列表中的datetime值
        
        :param dicts: 字典列表
        :return: 格式化后的字典列表
        """
        def _format_value(value: Any) -> Any:
            if isinstance(value, dict):
                return {k: _format_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [_format_value(item) for item in value]
            elif isinstance(value, datetime.datetime):
                return value.strftime(cls.DEFAULT_DATETIME_FORMAT)
            return value
            
        return [_format_value(item) for item in dicts]
