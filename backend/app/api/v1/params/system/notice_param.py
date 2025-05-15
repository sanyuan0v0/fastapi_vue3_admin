# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query

class NoticeQueryParams:
    """字典管理查询参数"""

    def __init__(
            self,
            notice_title: Optional[str] = Query(None, description="公告标题"),
            available: Optional[bool] = Query(None, description="是否可用"),
            creator: Optional[int] = Query(None, description="创建人"),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.notice_title = ("like", notice_title)

        # 精确查询字段
        self.creator_id = creator
        self.available = available

