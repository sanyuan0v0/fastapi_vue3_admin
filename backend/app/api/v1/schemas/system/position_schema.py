# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr

class PositionCreateSchema(BaseModel):
    """岗位创建模型"""
    name: str = Field(..., max_length=40, description="岗位名称")
    order: Optional[int] = Field(default=1, ge=1, description='显示排序')
    status: bool = Field(default=True, description="是否启用(True:启用 False:禁用)")
    description: Optional[str] = Field(None, description="备注说明")


class PositionUpdateSchema(PositionCreateSchema):
    """岗位更新模型"""
    id: int = Field(..., gt=0, description="岗位ID")


class PositionOutSchema(PositionCreateSchema, BaseSchema):
    """岗位信息响应模型"""
    model_config = ConfigDict(from_attributes=True)


class PositionOptionsOut(PositionCreateSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description="主键ID")
    created_at: DateTimeStr = Field(description="创建时间")
    updated_at: DateTimeStr = Field(description="更新时间")