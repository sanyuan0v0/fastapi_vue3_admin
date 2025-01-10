# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query


class ConfigQueryParams:
    """部门管理查询参数"""

    def __init__(
            self,
            title: Optional[str] = Query(None, description="网站标题", min_length=2, max_length=50),
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.title = ("like", title)


