# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class UploadResponseSchema(BaseModel):
    """
    上传响应模型
    """

    model_config = ConfigDict(from_attributes=True)

    file_path: Optional[str] = Field(default=None, description='新文件映射路径')
    file_name: Optional[str] = Field(default=None, description='新文件名称') 
    origin_name: Optional[str] = Field(default=None, description='原文件名称')
    file_url: Optional[str] = Field(default=None, description='新文件访问地址')


class FileListResponseSchema(BaseModel):
    """
    获取文件列表返回模型
    """
    model_config = ConfigDict(from_attributes=True)
    
    name: Optional[str] = Field(default=None, description='文件名称')
    type: Optional[str] = Field(default=None, description='文件类型')
    size: Optional[int] = Field(default=None, description='文件大小')
    modified_time: Optional[str] = Field(default=None, description='文件修改时间')
