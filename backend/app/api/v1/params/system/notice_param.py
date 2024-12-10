# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query

class NoticeQueryParams:
    """字典管理查询参数"""

    def __init__(
            self,
            notice_title: Optional[str] = Query(None, description="公告标题", min_length=2, max_length=20),
            available: Optional[bool] = Query(None, description="是否可用"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.notice_title = ("like", f"%{notice_title}%") if notice_title else None

        # 精确查询字段
        self.available = ("eq", available) if available is not None else None

