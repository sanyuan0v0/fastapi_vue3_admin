# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from fastapi import Query

class PositionQueryParams:
    """岗位管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="岗位名称"),
            available: Optional[bool] = Query(None, description="是否可用"),
            creator: Optional[int] = Query(None, description="创建人"),
            start_time: Optional[str] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[str] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", name)

        # 精确查询字段
        self.creator_id = creator
        self.available = available
        
        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))
