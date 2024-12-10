# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query
from datetime import datetime

from app.core.validator import DateTimeStr

class DeptQueryParams:
    """部门管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="部门名称", min_length=2, max_length=50),
            available: Optional[bool] = Query(None, description="部门状态(True正常 False停用)"),
            creator: Optional[str] = Query(None, description="创建者"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", f"%{name}%") if name else None
        self.creator = ("like", f"%{creator}%") if creator else None

        # 精确查询字段
        self.available = ("eq", available) if available is not None else None
        
        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))
