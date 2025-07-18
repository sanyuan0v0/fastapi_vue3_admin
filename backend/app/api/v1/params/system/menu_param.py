# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional, Literal
from fastapi import Query

from app.core.validator import DateTimeStr

class MenuQueryParams:
    """菜单管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="菜单名称"),
            route_path: Optional[str] = Query(None, description="路由地址"),
            component_path: Optional[str] = Query(None, description="组件路径"),
            type: Optional[Literal['M', 'C', 'F']] = Query(None, description="菜单类型(M目录 C菜单 F按钮)"),
            permission: Optional[str] = Query(None, description="权限标识"),
            status: Optional[bool] = Query(None, description="菜单状态(True正常 False停用)"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", name)
        self.route_path = ("like", route_path)
        self.component_path = ("like", component_path)
        self.permission = ("like", permission)

        # 精确查询字段
        self.type = type
        self.status = status

        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))

