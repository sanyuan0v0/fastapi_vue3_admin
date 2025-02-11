# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class GlobalDataCreateSchema(BaseModel):
    """全局参数模型"""
    name: str = Field(..., max_length=40, description="参数名称")
    value: str = Field(..., description="参数值")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    description: Optional[str] = Field(None, max_length=255, description="局参数描述")


class GlobalDataUpdateSchema(GlobalDataCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class GlobalDataOutSchema(GlobalDataCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
