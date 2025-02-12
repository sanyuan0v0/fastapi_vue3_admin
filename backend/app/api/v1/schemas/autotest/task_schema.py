# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class TaskCreateSchema(BaseModel):
    """执行记录模型"""
    name: str = Field(..., max_length=40, description="任务名称")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    description: Optional[str] = Field(None, max_length=255, description="环境描述")

    status: Optional[str] = Field(..., default="pedding", max_length=10, description="执行状态")
    
    start_time: Optional[str] = Field(None, description="开始时间")
    end_time: Optional[str] = Field(None, description="结束时间")
    summary: Optional[dict] = Field(None, description="报告摘要")

    total_count: Optional[int] = Field(None, ge=0, description="用例总数")
    success_count: Optional[int] = Field(None, ge=0, description="成功数")
    fail_count: Optional[int] = Field(None, ge=0, description="失败数")
    skip_count: Optional[int] = Field(None, ge=0, description="跳过数")
    error_count: Optional[int] = Field(None, ge=0, description="错误数")

    logs: Optional[list] = Field(None, description="执行日志")
    actual_response: Optional[dict] = Field(None, description="实际响应（仅API测试）")

class TaskUpdateSchema(TaskCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")
    

class TaskOutSchema(TaskCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)

    project: Optional[dict] = Field(None, description="所属项目信息")