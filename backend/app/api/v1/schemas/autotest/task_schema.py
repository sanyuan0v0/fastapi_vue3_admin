# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class TaskCreateSchema(BaseModel):
    """执行记录模型"""
    test_case_id: int = Field(..., gt=0, description="关联的测试用例ID")
    status: str = Field(..., max_length=10, description="执行状态")
    logs: Optional[list] = Field(None, description="执行日志")
    actual_response: Optional[dict] = Field(None, description="实际响应（仅API测试）")
    description: Optional[str] = Field(None, max_length=255, description="环境描述")


class TaskUpdateSchema(TaskCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class TaskOutSchema(TaskCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
