# -*- coding: utf-8 -*-

from typing import Optional, Literal
from fastapi import Query


class MenuQueryParams:
    """菜单管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="菜单名称", min_length=2, max_length=50),
            route_path: Optional[str] = Query(None, description="路由地址", min_length=1, max_length=200),
            component_path: Optional[str] = Query(None, description="组件路径", min_length=1, max_length=200),
            type: Optional[Literal['M', 'C', 'F']] = Query(None, description="菜单类型(M目录 C菜单 F按钮)"),
            permission: Optional[str] = Query(None, description="权限标识", min_length=1, max_length=100),
            available: Optional[bool] = Query(None, description="菜单状态(True正常 False停用)"),
            creator: Optional[str] = Query(None, description="创建者"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", f"%{name}%") if name else None
        self.route_path = ("like", f"%{route_path}%") if route_path else None
        self.component_path = ("like", f"%{component_path}%") if component_path else None
        self.permission = ("like", f"%{permission}%") if permission else None
        self.creator = ("like", f"%{creator}%") if creator else None

        # 精确查询字段
        self.type = ("eq", type) if type else None
        self.available = ("eq", available) if available is not None else None
