# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query
from datetime import datetime

from app.core.validator import DateTimeStr


class DictTypeQueryParams:
    """操作日志查询参数"""

    def __init__(
            self,
            dict_name: Optional[str] = Query(None, description="字典名称"),
            dict_type: Optional[str] = Query(None, description="字典类型"),
            available: Optional[bool] = Query(None, description="状态（0正常 1停用）"),
            creator: Optional[int] = Query(None, description="创建人"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.dict_name = ("like", f"%{dict_name}%") if dict_name else None
        
        # 精确查询字段
        self.creator_id = creator
        self.dict_type = dict_type
        self.available = available
        
        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))


class DictDataQueryParams:
    """操作日志查询参数"""

    def __init__(
            self,
            dict_label: Optional[str] = Query(None, description="字典标签"),
            dict_type: Optional[str] = Query(None, description="字典类型"),
            available: Optional[bool] = Query(None, description="状态（0正常 1停用）"),
            creator: Optional[int] = Query(None, description="创建人"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.dict_label = ("like", f"%{dict_label}%") if dict_label else None
        
        # 精确查询字段
        self.creator_id = creator
        self.dict_type = dict_type
        self.available = available
        
        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))