# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query
from datetime import datetime

from app.core.validator import DateTimeStr

class OperationLogQueryParams:
    """操作日志查询参数"""

    def __init__(
            self,
            request_path: Optional[str] = Query(None, description="请求路径"),
            request_method: Optional[str] = Query(None, description="请求方法"),
            request_ip: Optional[str] = Query(None, description="请求IP"),
            response_code: Optional[int] = Query(None, description="响应状态码"),
            creator: Optional[int] = Query(None, description="创建人"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.request_path = ("like", f"%{request_path}%") if request_path else None
        
        # 精确查询字段
        self.creator_id = creator
        self.request_method = request_method
        self.request_ip = request_ip
        self.response_code = response_code
        
        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))
