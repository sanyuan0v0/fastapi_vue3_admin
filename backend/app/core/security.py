# -*- coding: utf-8 -*-

import jwt
from typing import Dict, Optional
from fastapi import Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param

from app.core.exceptions import CustomException
from app.api.v1.schemas.system.auth_schema import JWTPayloadSchema
from app.config.setting import settings


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    """自定义OAuth2认证类,继承自OAuth2PasswordBearer"""

    def __init__(
            self,
            token_url: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True
    ) -> None:
        super().__init__(
            tokenUrl=token_url,
            scheme_name=scheme_name,
            scopes=scopes,
            description=description,
            auto_error=auto_error
        )

    async def __call__(self, request: Request) -> Optional[str]:
        """重写认证方法,校验token"""
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != settings.TOKEN_TYPE:
            if self.auto_error:
                raise CustomException(msg="请登录后再试")
            return None
        return token


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    """自定义登录表单,扩展验证码等字段"""

    def __init__(
            self,
            grant_type: str | None = Form(default=None, regex='password'),
            scope: str = Form(default=''),
            client_id: Optional[str] = Form(default=None),
            client_secret: Optional[str] = Form(default=None),
            username: str = Form(),
            password: str = Form(),
            captcha_key: Optional[str] = Form(default=""),
            captcha: Optional[str] = Form(default=""),
    ):
        super().__init__(
            grant_type=grant_type,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password
        )
        self.captcha_key = captcha_key
        self.captcha = captcha


# OAuth2认证配置
OAuth2Schema = CustomOAuth2PasswordBearer(
    token_url="system/auth/login",
    description="认证"
)


def create_access_token(payload: JWTPayloadSchema) -> str:
    """生成JWT访问令牌"""
    payload_dict = payload.model_dump()
    return jwt.encode(
        payload=payload_dict,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_access_token(token: str) -> JWTPayloadSchema:
    """解析JWT访问令牌"""
    if not token:
        raise CustomException(msg="认证不存在,请重新登录", status_code=403)

    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        username = payload.get("sub")
        if not username:
            raise CustomException(msg="无效认证,请重新登录", status_code=403)

        return JWTPayloadSchema(**payload)

    except (jwt.InvalidSignatureError, jwt.DecodeError):
        raise CustomException(msg="无效认证,请重新登录", status_code=403)

    except jwt.ExpiredSignatureError:
        raise CustomException(msg="认证已过期,请重新登录", status_code=403)

    except jwt.InvalidTokenError:
        raise CustomException(msg="token已失效,请重新登录", status_code=403)
