# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class ReportCreateSchema(BaseModel):
    """测试报告模型"""
    name: str = Field(..., max_length=40, description="测试报告名称")
    task_id: int = Field(..., gt=0, description="关联的任务ID")
    summary: dict = Field(..., description="报告摘要")
    details: dict = Field(..., description="详细报告")
    description: Optional[str] = Field(None, max_length=255, description="通知配置描述")


class ReportUpdateSchema(ReportCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class ReportOutSchema(ReportCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
