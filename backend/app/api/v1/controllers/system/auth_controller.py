# -*- coding: utf-8 -*-

from typing import Union, Dict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.setting import settings
from app.common.response import ErrorResponse, SuccessResponse
from app.api.v1.services.system.auth_service import (
    LoginService,
    CaptchaService
)
from app.api.v1.schemas.system.auth_schema import (
    CaptchaOutSchema,
    JWTOutSchema,
    RefreshTokenPayloadSchema,
    LogoutPayloadSchema
)
from app.core.dependencies import (
    db_getter,
    get_current_user
)
from app.core.router_class import OperationLogRoute
from app.core.security import CustomOAuth2PasswordRequestForm
from app.core.logger import logger


router = APIRouter(route_class=OperationLogRoute)


@router.post("/login", summary="登录", description="登录",response_model=JWTOutSchema)
async def login_for_access_token(
        request: Request,
        login_form: CustomOAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(db_getter),
) -> Union[JSONResponse, Dict]:
    user = await LoginService.authenticate_user(request=request, login_form=login_form, db=db)
    login_token = await LoginService.create_token(request=request, username=user.username)
    logger.info(f"用户{user.username}登录成功")
    
    # 如果是文档请求，则不记录日志:http://localhost:8000/api/v1/docs
    if settings.DOCS_URL in request.headers.get("referer", ""):
        return login_token.model_dump()
    return SuccessResponse(data=login_token.model_dump(), msg="登录成功")


@router.post("/token/refresh", summary="刷新token", description="刷新token", response_model=JWTOutSchema, dependencies=[Depends(get_current_user)])
async def get_new_token(
        request: Request,
        payload: RefreshTokenPayloadSchema
) -> JSONResponse:
    # 解析当前的访问Token以获取用户名
    new_token = await LoginService.refresh_token(request=request, refresh_token=payload)
    token_dict = new_token.model_dump()
    logger.info(f"刷新token成功: {token_dict}")
    return SuccessResponse(data=token_dict, msg="刷新成功")


@router.post("/captcha/get", summary="获取验证码", description="获取登录验证码", response_model=CaptchaOutSchema)
async def get_captcha_for_login(
        request: Request
) -> JSONResponse:
    # 获取验证码
    captcha = await CaptchaService.get_captcha(request=request)
    logger.info(f"获取验证码成功")
    return SuccessResponse(data=captcha, msg="获取验证码成功")


@router.post('/logout', summary="退出登录", description="退出登录", dependencies=[Depends(get_current_user)])
async def logout(
    request: Request,
    payload: LogoutPayloadSchema
) -> JSONResponse:
    if await LoginService.logout_services(request=request, token=payload):
        logger.info('退出成功')
        return SuccessResponse(msg='退出成功')
    return ErrorResponse(msg='退出失败')    
