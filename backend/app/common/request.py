# -*- coding: utf-8 -*-

import math
from typing import Any, Dict, List, Optional
from pydantic import ConfigDict, Field, BaseModel
from pydantic.alias_generators import to_camel

from app.common.constant import RET
from app.core.exceptions import CustomException


class PageResultSchema(BaseModel):
    """分页查询结果模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    page_no: Optional[int] = Field(default=None, ge=1, description="页码，默认为1")
    page_size: Optional[int] = Field(default=None, ge=1, description="页面大小，默认为10") 
    total: int = Field(default=0, ge=0, description="总记录数")
    has_next: Optional[bool] = Field(default=False, description="是否有下一页")
    items: List[Any] = Field(default_factory=list, description="分页后的数据列表")


class PaginationService:
    """分页服务类"""

    @staticmethod
    async def get_page_obj(data_list: List[Any], page_no: Optional[int] = None, page_size: Optional[int] = None) -> Dict[str, Any]:
        """
        输入数据列表data_list和分页信息，返回分页或非分页数据列表结果。
        如果未传入page_no和page_size，则返回全部数据。

        :param data_list: 原始数据列表
        :param page_no: 当前页码,默认为None
        :param page_size: 当前页面数据量,默认为None
        :return: 分页或非分页数据对象
        :raises: CustomException 当分页参数不合法时抛出
        """
        total = len(data_list)

        # 如果page_no和page_size都为None,返回全部数据
        if page_no is None or page_size is None:
            return {
                "items": data_list,
                "total": total,
                "page_no": None,
                "page_size": None,
                "has_next": False
            }

        # 验证分页参数
        if page_no < 1 or page_size < 1:
            raise CustomException(code=RET.BAD_REQUEST.code, msg="分页参数不合法")
        
        # 计算起始索引和结束索引
        start = (page_no - 1) * page_size
        end = min(start + page_size, total)

        # 根据计算得到的起始索引和结束索引对数据列表进行切片
        paginated_data = data_list[start:end]

        # 判断是否有下一页
        has_next = end < total

        return {
            "items": paginated_data,
            "total": total,
            "page_no": page_no,
            "page_size": page_size,
            "has_next": has_next
        }