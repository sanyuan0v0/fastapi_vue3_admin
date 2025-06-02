# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query


class ConfigQueryParams:
    """配置管理查询参数"""

    def __init__(
            self,
            config_name: Optional[str] = Query(None, description="配置名称"),
            config_key: Optional[str] = Query(None, description="配置键名"),
            config_type: Optional[bool] = Query(None, description="系统内置((True:是 False:否))"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.config_name = ("like", config_name)
        self.config_key = ("like", config_key)

        # 精确查询字段
        self.config_type = config_type


