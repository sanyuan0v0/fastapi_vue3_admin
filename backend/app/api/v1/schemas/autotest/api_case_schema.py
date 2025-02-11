# -*- coding: utf-8 -*-


from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.core.base_schema import BaseSchema


class APICaseCreateSchema(BaseModel):
    """接口测试用例创建模型"""
    name: str = Field(..., max_length=50, description='测试用例名称')
    url: str = Field(..., max_length=255, description="接口地址")
    method: str = Field(..., max_length=10, description="请求方法")
    headers: Optional[str] = Field(None, description="请求头")
    data_type: Optional[str] = Field(None, description="请求参数类型(params/data/json/file)")
    data: Optional[str] = Field(None, description="请求体")
    
    expected_status_code: int = Field(..., gt=0, description="预期状态码")
    expected_msg: Optional[str] = Field(None, description="预期消息")
    expected_response: Optional[str] = Field(None, description="预期响应")
    assertions_status_code: Optional[str] = Field(None, description="状态码断言规则(=, !=, >, <, >=, <=, in, not in)")
    assertions_msg: Optional[str] = Field(None, description="消息断言规则(=, !=, >, <, >=, <=, in, not in)")
    assertions_response: Optional[str] = Field(None, description="响应断言规则(=, !=, >, <, >=, <=, in, not in)")

    description: Optional[str] = Field(None, max_length=255, description="测试用例描述")
    environment_id: int = Field(..., gt=0, description="所属环境ID")
    global_data_id: Optional[int] = Field(None, gt=0, description="关联全局数据ID")
    module_id: int = Field(..., gt=0, description="所属模块ID")
    project_id: int = Field(..., gt=0, description="所属项目ID")


class APICaseUpdateSchema(APICaseCreateSchema):
    """接口测试用例更新模型"""
    id: int = Field(..., gt=0, description="接口测试用例ID")


class APICaseOutSchema(APICaseCreateSchema, BaseSchema):
    """接口测试用例响应模型"""
    model_config = ConfigDict(from_attributes=True)

