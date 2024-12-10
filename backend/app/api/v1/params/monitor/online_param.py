# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query
from datetime import datetime

from app.core.validator import DateTimeStr


class OnlineQueryParams:
    """在线用户查询参数"""

    def __init__(
            self,
            user_name: Optional[str] = Query(None, description="登录名称"), 
            ipaddr: Optional[str] = Query(None, description="登陆IP地址"),
            login_location: Optional[str] = Query(None, description="登录所属地"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.user_name = ("like", f"%{user_name}%") if user_name else None
        self.login_location = ("like", f"%{login_location}%") if login_location else None

        # 精确查询字段
        self.ipaddr = ("eq", ipaddr) if ipaddr else None
