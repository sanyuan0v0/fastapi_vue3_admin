# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class NotificationConfigCreateSchema(BaseModel):
    """通知配置模型"""
    name: str = Field(..., max_length=40, description="通知类型（邮件、钉钉、Slack等）")
    config: dict = Field(..., description="通知配置")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    description: Optional[str] = Field(None, max_length=255, description="通知配置描述")


class NotificationConfigUpdateSchema(NotificationConfigCreateSchema):
    """接口更新模型"""
    id: int = Field(..., gt=0, description="接口ID")


class NotificationConfigOutSchema(NotificationConfigCreateSchema, BaseSchema):
    """接口响应模型"""
    model_config = ConfigDict(from_attributes=True)
