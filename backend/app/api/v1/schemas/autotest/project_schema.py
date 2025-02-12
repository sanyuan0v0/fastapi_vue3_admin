# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class ProjectCreateSchema(BaseModel):
    """项目创建模型"""
    name: str = Field(..., description="项目名称")
    base_url: str = Field(..., description="基础URL")
    headers: Optional[dict] = Field(None, description="公共请求头")
    message: Optional[dict] = Field(None, description="通知配置")
    description: Optional[str] = Field(None, description="备注说明")


class ProjectUpdateSchema(ProjectCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class ProjectOutSchema(ProjectCreateSchema, BaseSchema):
    """项目响应模型"""
    model_config = ConfigDict(from_attributes=True)

    cases: Optional[list] = Field(None, description="关联的用例")
    tasks: Optional[list] = Field(None, description="关联的任务")
