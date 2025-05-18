# -*- coding: utf-8 -*-

import time
from typing import Dict, List, Union
from fastapi import status
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp
from starlette.requests import Request
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.base import (
    Response,
    BaseHTTPMiddleware,
    RequestResponseEndpoint
)

from app.common.response import ErrorResponse
from app.config.setting import settings
from app.core.logger import logger
from app.core.exceptions import CustomException


class CustomCORSMiddleware(CORSMiddleware):
    """CORS跨域中间件"""
    def __init__(self, app: ASGIApp) -> None:
        CORSMiddlewareConfig: Dict[str, Union[List[str], bool]] = {
            "allow_origins": settings.ALLOW_ORIGINS,
            "allow_methods": settings.ALLOW_METHODS,
            "allow_headers": settings.ALLOW_HEADERS,
            "allow_credentials": settings.ALLOW_CREDENTIALS
        }
        super().__init__(app, **CORSMiddlewareConfig)


class RequestLogMiddleware(BaseHTTPMiddleware):
    """
    记录请求日志中间件: 提供一个基础的中间件类，允许你自定义请求和响应处理逻辑。
    """
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()
        
        logger.info(
            f"请求来源: {request.client.host}, "
            f"请求方法: {request.method}, "
            f"请求路径: {request.url.path}, "
            f"客户端IP: {request.client.host}"
        )
        
        try:
            response = await call_next(request)
            process_time = round(time.time() - start_time, 5)
            response.headers["X-Process-Time"] = str(process_time)
            
            logger.info(
                f"响应状态: {response.status_code}, "
                f"响应内容长度: {response.headers.get('content-length', '0')}, "
                f"处理时间: {process_time}s"
            )
            
            return response
        
        except CustomException as e:
            logger.error(f"系统异常: {str(e)}")
            return ErrorResponse(msg=f"系统异常，请联系管理员: {str(e)}")


class DemoEnvMiddleware(BaseHTTPMiddleware):
    """演示环境中间件"""
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if settings.DEMO_ENABLE and request.method != "GET":
            path = request.scope.get("path")
            if path in settings.DEMO_BLACK_LIST_PATH:
                return ErrorResponse(msg="演示环境，禁止操作",)
            elif path not in settings.DEMO_WHITE_LIST_PATH:
                return ErrorResponse(msg="演示环境，禁止操作",)

        return await call_next(request)


class CustomGZipMiddleware(GZipMiddleware):
    """GZip压缩中间件"""
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            minimum_size=settings.GZIP_MIN_SIZE,
            compresslevel=settings.GZIP_COMPRESS_LEVEL
        )

