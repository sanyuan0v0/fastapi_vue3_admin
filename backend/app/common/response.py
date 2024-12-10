# -*- coding: utf-8 -*-

from typing import Any, Optional
from fastapi import status
from fastapi.responses import JSONResponse, StreamingResponse
from app.common.constant import RET
from pydantic import Field, BaseModel

class ResponseSchema(BaseModel):
    """响应模型"""
    code: int = Field(default=RET.OK.code, description="业务状态码")
    msg: str = Field(default=RET.OK.msg, description="响应消息")
    data: Optional[Any] = Field(default=None, description="响应数据")
    status_code: int = Field(default=status.HTTP_200_OK, description="HTTP状态码")

class SuccessResponse(JSONResponse):
    """成功响应类"""

    def __init__(
            self,
            data: Optional[Any] = None,
            msg: Optional[str] = RET.OK.msg,
            code: int = RET.OK.code,
            status_code: int = status.HTTP_200_OK,
    ) -> None:
        """
        初始化成功响应类
        
        :param data: 响应数据
        :param msg: 响应消息
        :param code: 业务状态码
        :param status_code: HTTP状态码
        """
        content = ResponseSchema(
            code=code,
            msg=msg,
            data=data,
            status_code=status_code
        ).model_dump()
        super().__init__(content=content, status_code=status_code)


class ErrorResponse(JSONResponse):
    """错误响应类"""

    def __init__(
            self,
            data: Optional[Any] = None,
            msg: Optional[str] = RET.ERROR.msg,
            code: int = RET.ERROR.code,
            status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        """
        初始化错误响应类
        
        :param data: 响应数据
        :param msg: 响应消息
        :param code: 业务状态码
        :param status_code: HTTP状态码
        """
        content = ResponseSchema(
            code=code,
            msg=msg,
            data=data,
            status_code=status_code
        ).model_dump()
        super().__init__(content=content, status_code=status_code)


class StreamResponse(StreamingResponse):
    """流式响应类"""

    def __init__(
            self,
            data: Optional[Any] = None,
            msg: Optional[str] = RET.OK.msg,
            code: int = RET.OK.code,
            status_code: int = status.HTTP_200_OK,
    ) -> None:
        """
        初始化流式响应类
        
        :param data: 响应数据
        :param msg: 响应消息
        :param code: 业务状态码
        :param status_code: HTTP状态码
        """
        content = ResponseSchema(
            code=code,
            msg=msg,
            data=data,
            status_code=status_code
        ).model_dump()
        super().__init__(content=content, status_code=status_code)
