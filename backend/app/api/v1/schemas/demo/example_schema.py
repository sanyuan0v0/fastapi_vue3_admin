# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class ExampleCreateSchema(BaseModel):
    """新增模型"""
    name: str = Field(..., max_length=50, description='名称')
    status: bool = Field(True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(None, max_length=255, description="描述")


class ExampleUpdateSchema(ExampleCreateSchema):
    """更新模型"""
    id: int = Field(..., gt=0, description="示例ID")


class ExampleOutSchema(ExampleCreateSchema, BaseSchema):
    """响应模型"""
    model_config = ConfigDict(from_attributes=True)
