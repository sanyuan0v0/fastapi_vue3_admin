# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query

class PositionQueryParams:
    """岗位管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="岗位名称", min_length=2, max_length=20),
            available: Optional[bool] = Query(None, description="是否可用"),
            start_time: Optional[str] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[str] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", f"%{name}%") if name else None

        # 精确查询字段
        self.available = ("eq", available) if available is not None else None
        
        # 时间范围查询
        self.created_at = ("between", [start_time, end_time]) if start_time and end_time else None
