# -*- coding: utf-8 -*-

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ConfigCreateSchema(BaseModel):
    """配置创建模型"""

    name: str = Field(..., max_length=40, description="配置名称")
    order: int = Field(default=1, ge=0, description="显示顺序")
    fied_key: str = Field(..., description="键")
    fied_value: Optional[str] = Field(default=None, description="值")
    parent_id: Optional[int] = Field(default=None, ge=0, description="父配置ID")

    @classmethod
    @model_validator(mode='after')
    def validate_fields(cls, data):
        if not data.name or len(data.name.strip()) == 0:
            raise ValueError("配置名称不能为空")
        return data


class ConfigUpdateSchema(ConfigCreateSchema):
    """配置更新模型"""
    id: int = Field(description="主键ID")


class ConfigOutSchema(ConfigCreateSchema):
    """配置响应模型"""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="主键ID")
