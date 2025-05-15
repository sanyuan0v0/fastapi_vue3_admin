# -*- coding: utf-8 -*-

from typing import Optional, Literal
from fastapi import Query


class MenuQueryParams:
    """菜单管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="菜单名称"),
            route_path: Optional[str] = Query(None, description="路由地址"),
            component_path: Optional[str] = Query(None, description="组件路径"),
            type: Optional[Literal['M', 'C', 'F']] = Query(None, description="菜单类型(M目录 C菜单 F按钮)"),
            permission: Optional[str] = Query(None, description="权限标识"),
            available: Optional[bool] = Query(None, description="菜单状态(True正常 False停用)"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", name)
        self.route_path = ("like", route_path)
        self.component_path = ("like", component_path)
        self.permission = ("like", permission)

        # 精确查询字段
        self.type = type
        self.available = available
