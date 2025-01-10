# -*- coding: utf-8 -*-

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.base_schema import BaseSchema


class ConfigCreateSchema(BaseModel):
    """配置创建模型"""

    title: str = Field(..., max_length=40, description="网站标题")
    favicon: str = Field(..., max_length=100, description="网站favicon")
    logo: str = Field(..., max_length=100, description="网站logo")
    background: str = Field(..., max_length=100, description="网站背景")
    description: str = Field(..., max_length=100, description="网站描述")
    copyright: str = Field(..., max_length=100, description="版权信息")
    keep_record: str = Field(..., max_length=100, description="备案信息")
    help_url: str = Field(..., max_length=100, description="帮助链接")
    privacy_url: str = Field(..., max_length=100, description="隐私政策链接")
    clause_url: str = Field(..., max_length=100, description="服务条款链接")
    code_url: str = Field(..., max_length=100, description="源码地址")


class ConfigUpdateSchema(ConfigCreateSchema):
    """配置更新模型"""
    id: int = Field(description="主键ID")


class ConfigOutSchema(ConfigCreateSchema, BaseSchema):
    """配置响应模型"""
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="主键ID")
