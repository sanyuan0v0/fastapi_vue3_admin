# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class EnvironmentCreateSchema(BaseModel):
    """环境模型"""
    name: str = Field(..., max_length=50, description='环境名称')
    base_url: str = Field(..., max_length=255, description="基础URL")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    description: Optional[str] = Field(None, max_length=255, description="环境描述")


class EnvironmentUpdateSchema(EnvironmentCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class EnvironmentOutSchema(EnvironmentCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
