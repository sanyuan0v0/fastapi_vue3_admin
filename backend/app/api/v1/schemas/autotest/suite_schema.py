# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class SuiteCreateSchema(BaseModel):
    """套件模型"""
    name: str = Field(..., max_length=40, description="套件名称")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    description: Optional[str] = Field(None, max_length=255, description="通知配置描述")


class SuiteUpdateSchema(SuiteCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class SuiteOutSchema(SuiteCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
