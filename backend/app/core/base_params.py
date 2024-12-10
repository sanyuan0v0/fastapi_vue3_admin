# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query


class PaginationQueryParams:
    """分页查询参数基类"""

    def __init__(
            self,
            page_no: Optional[int] = Query(default=None, description="当前页码", ge=1),
            page_size: Optional[int] = Query(default=None, description="每页数量", ge=1, le=100), 
            order_by: Optional[str] = Query(default=None, description="排序字段,格式:[{'field':'asc/desc'}]"),
    ) -> None:
        """
        初始化分页查询参数
        
        :param page_no: 当前页码,默认None
        :param page_size: 每页数量,默认None,最大100
        :param order_by: 排序字段
        """
        self.page_no = page_no
        self.page_size = page_size
        self.order_by = order_by

