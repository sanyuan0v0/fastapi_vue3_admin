# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional
from fastapi import Query

from app.core.validator import DateTimeStr

class ConfigQueryParams:
    """配置管理查询参数"""

    def __init__(
            self,
            config_name: Optional[str] = Query(None, description="配置名称"),
            config_key: Optional[str] = Query(None, description="配置键名"),
            config_type: Optional[bool] = Query(None, description="系统内置((True:是 False:否))"),
            start_time: Optional[DateTimeStr] = Query(None, description="开始时间", example="2023-01-01 00:00:00"),
            end_time: Optional[DateTimeStr] = Query(None, description="结束时间", example="2023-12-31 23:59:59"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.config_name = ("like", config_name)
        self.config_key = ("like", config_key)

        # 精确查询字段
        self.config_type = config_type

        # 时间范围查询
        if start_time and end_time:
            start_datetime = datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S')
            end_datetime = datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')
            self.created_at = ("between", (start_datetime, end_datetime))


