# -*- coding: utf-8 -*-

from typing import Any, Optional
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic_validation_decorator import FieldValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.common.response import ErrorResponse
from app.core.logger import logger


class CustomException(Exception):
    """自定义异常基类"""

    def __init__(
            self,
            msg: Optional[str] = "exception",
            code: int = -1,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            data: Optional[Any] = None,
    ) -> None:
        """
        初始化异常
        :param msg: 错误消息
        :param code: 业务状态码
        :param status_code: HTTP状态码
        :param data: 附加数据
        """
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.data = data


async def CustomExceptionHandler(request: Request, exc: CustomException) -> JSONResponse:
    """自定义异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误信息: {exc.msg}, 错误详情: {exc.data}")
    return ErrorResponse(msg=exc.msg, code=exc.code, status_code=exc.status_code, data=exc.data)


async def HttpExceptionHandler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误详情: {exc.detail}")
    return ErrorResponse(msg=exc.detail, status_code=exc.status_code)


async def ValidationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求参数验证异常处理器"""
    error_mapping = {
        "Field required": "请求失败，缺少必填项！",
        "value is not a valid list": "类型错误，提交参数应该为列表！", 
        "value is not a valid int": "类型错误，提交参数应该为整数！",
        "value could not be parsed to a boolean": "类型错误，提交参数应该为布尔值！",
        "Input should be a valid list": "类型错误，输入应该是一个有效的列表！"
    }
    
    msg = error_mapping.get(exc.errors()[0].get('msg'), exc.errors()[0].get('msg'))
    logger.error(f"请求地址: {request.url}, 错误信息: {msg}, 错误详情: {exc}")
    return ErrorResponse(msg=msg, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, data=exc.body)

async def ResponseValidationHandle(request: Request, exc: ResponseValidationError) -> JSONResponse:
    logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
    return ErrorResponse(msg=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=exc.body)

async def SQLAlchemyExceptionHandler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """数据库异常处理器"""
    error_msg = f'数据库操作失败: {exc}'
    logger.error(f"请求地址: {request.url}, 错误详情: {error_msg}")
    return ErrorResponse(msg=error_msg, status_code=status.HTTP_400_BAD_REQUEST, data=str(exc))


async def ValueExceptionHandler(request: Request, exc: ValueError) -> JSONResponse:
    """值异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
    return ErrorResponse(msg=str(exc))


async def FieldValidationExceptionHandler(request: Request, exc: FieldValidationError) -> JSONResponse:
    """字段验证异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误信息: {exc.message}, 错误详情: {exc}")
    return ErrorResponse(msg=str(exc))


async def AllExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理器"""
    logger.error(f"请求地址: {request.url}, 错误详情: {exc}")
    return ErrorResponse(msg='服务器内部错误', status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data=str(exc))
