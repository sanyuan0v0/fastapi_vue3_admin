# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from fastapi import Query



class UserQueryParams:
    """用户管理查询参数"""

    def __init__(
            self,
            username: Optional[str] = Query(None, description="用户名"),
            name: Optional[str] = Query(None, description="名称"),
            mobile: Optional[str] = Query(None, description="手机号", pattern=r'^1[3-9]\d{9}$'),
            email: Optional[str] = Query(None, description="邮箱", pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'), 
            dept_id: Optional[int] = Query(None, description="部门ID"),
            available: Optional[bool] = Query(None, description="是否可用"),
            start_time: Optional[str] = Query(None, description="开始时间"),
            end_time: Optional[str] = Query(None, description="结束时间"),
            creator: Optional[int] = Query(None, description="创建人"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.username = ("like", username)
        self.name = ("like", name)
        self.mobile = ("like", mobile)
        self.email = ("like", email)

        # 精确查询字段
        self.dept_id = dept_id
        self.creator_id = creator
        self.available = available
        
        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))
