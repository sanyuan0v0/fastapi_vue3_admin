# -*- coding: utf-8 -*-

from datetime import date
from typing import Optional, Union
from fastapi import Query


class BaseQueryParams:
    """股票基础查询参数"""
    def __init__(
            self,
            name: Optional[str] = Query(None, description="名称"),
            code: Optional[str] = Query(None, description="代码"),
            start_date: Optional[Union[str, date]] = Query(None, description="日期", example="2025-08-01"),
            end_date: Optional[Union[str, date]] = Query(None, description="日期", example="2025-08-31"),
    ) -> None:
        super().__init__()
        # 模糊查询字段
        self.name = ("like", name)

        # 精确查询字段
        self.code = code

        # 时间范围查询
        if start_date and end_date:
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            self.date = ("between", (start_date, end_date))
