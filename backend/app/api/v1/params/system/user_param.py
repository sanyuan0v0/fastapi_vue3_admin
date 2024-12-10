# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query



class UserQueryParams:
    """用户管理查询参数"""

    def __init__(
            self,
            username: Optional[str] = Query(None, description="用户名", min_length=2, max_length=20),
            name: Optional[str] = Query(None, description="名称", min_length=2, max_length=20),
            mobile: Optional[str] = Query(None, description="手机号", pattern=r'^1[3-9]\d{9}$'),
            email: Optional[str] = Query(None, description="邮箱", pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'), 
            available: Optional[bool] = Query(None, description="是否可用"),
            start_time: Optional[str] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[str] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.username = ("like", f"%{username}%") if username else None
        self.name = ("like", f"%{name}%") if name else None
        self.mobile = ("like", f"%{mobile}%") if mobile else None
        self.email = ("like", f"%{email}%") if email else None

        # 精确查询字段
        self.available = ("eq", available) if available is not None else None
        
        # 时间范围查询
        self.created_at = ("between", [start_time, end_time]) if start_time and end_time else None
