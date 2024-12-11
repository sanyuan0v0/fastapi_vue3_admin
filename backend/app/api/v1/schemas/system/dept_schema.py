# -*- coding: utf-8 -*-

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.base_schema import BaseSchema
from app.core.validator import DateTimeStr

class DeptCreateSchema(BaseModel):
    """部门创建模型"""

    name: str = Field(..., max_length=40, description="部门名称")
    order: int = Field(default=1, ge=0, description="显示顺序")
    available: bool = Field(default=True, description="是否启用(True:启用 False:禁用)")
    parent_id: Optional[int] = Field(default=None, ge=0, description="父部门ID")
    description: Optional[str] = Field(default=None, max_length=500, description="备注说明")

    @classmethod
    @model_validator(mode='after')
    def validate_fields(cls, data):
        if not data.name or len(data.name.strip()) == 0:
            raise ValueError("部门名称不能为空")
        return data


class DeptUpdateSchema(DeptCreateSchema):
    """部门更新模型"""
    id: int = Field(..., gt=0, description="部门ID")


class DeptOutSchema(DeptCreateSchema):
    """部门响应模型"""
    model_config = ConfigDict(from_attributes=True)

    parent_name: Optional[str] = Field(default=None, max_length=40, description="父部门名称")
    id: int = Field(description="主键ID")
    created_at: DateTimeStr = Field(description="创建时间")
    updated_at: DateTimeStr = Field(description="更新时间")