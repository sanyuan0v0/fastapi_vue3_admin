# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class CaseCreateSchema(BaseModel):
    """接口测试用例创建模型"""
    name: str = Field(..., description='测试用例名称')
    status: Optional[bool] = Field(True, description='是否启用')
    url: str = Field(..., description="接口地址")
    method: str = Field(..., description="请求方法")
    headers: Optional[dict] = Field(None, description="请求头")
    params: Optional[dict] = Field(None, description="Query参数")
    body: Optional[dict] = Field(None, description="请求体")
    files: Optional[dict] = Field(None, description="上传文件配置")
    parameter_need: bool = Field(True, description="是否需要公共参数")
    expected: Optional[list] = Field(None, description="断言配置")
    project_id: int = Field(..., gt=0, description="所属项目ID")
    
    description: Optional[str] = Field(None, description="备注说明")


class CaseUpdateSchema(CaseCreateSchema):
    """接口测试用例更新模型"""
    id: int = Field(..., gt=0, description="接口测试用例ID")


class CaseOutSchema(CaseCreateSchema, BaseSchema):
    """接口测试用例响应模型"""
    model_config = ConfigDict(from_attributes=True)
    
    project: Optional[dict] = Field(None, description="所属项目信息")

