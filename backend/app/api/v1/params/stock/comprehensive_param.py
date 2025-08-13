# -*- coding: utf-8 -*-

from datetime import date
from typing import Optional, Union

from fastapi import Query
from app.api.v1.params.stock.base_param import BaseQueryParams

class ComprehensiveQueryParams(BaseQueryParams):
    """综合选股查询参数"""
    def __init__(
            self,
            name: Optional[str] = Query(None, description="名称"),
            code: Optional[str] = Query(None, description="代码"),
            start_date: Optional[Union[str, date]] = Query(None, description="开始日期", example="2023-01-01"),
            end_date: Optional[Union[str, date]] = Query(None, description="结束日期", example="2023-01-01"),

    ) -> None:
        super().__init__(name, code, start_date, end_date)

