# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class ModuleCreateSchema(BaseModel):
    """模块模型"""
    name: str = Field(..., max_length=40, description="模块名称")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    description: Optional[str] = Field(None, max_length=255, description="模块描述")


class ModuleUpdateSchema(ModuleCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class ModuleOutSchema(ModuleCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
