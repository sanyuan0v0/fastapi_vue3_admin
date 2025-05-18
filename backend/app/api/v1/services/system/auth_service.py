# -*- coding: utf-8 -*-

from typing import Dict, Union, NewType
from fastapi import Request
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from user_agents import parse

from app.common.enums import RedisInitKeyConfig
from app.core.logger import logger
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.api.v1.schemas.monitor.online_schema import OnlineOutSchema
from app.utils.common_util import get_random_character
from app.utils.captcha_util import CaptchaUtil
from app.api.v1.cruds.system.user_crud import UserCRUD
from app.api.v1.models.system.user_model import UserModel
from app.api.v1.schemas.system.auth_schema import (
    JWTPayloadSchema,
    JWTOutSchema,
    AuthSchema,
    CaptchaOutSchema,
    LogoutPayloadSchema,
    RefreshTokenPayloadSchema
)
from app.core.hash_bcrpy import PwdUtil
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    create_access_token,
    decode_access_token
)
from app.utils.ip_local_util import IpLocalUtil
from app.core.redis_crud import RedisCURD

CaptchaKey = NewType('CaptchaKey', str)
CaptchaBase64 = NewType('CaptchaBase64', str)


class LoginService:
    """登录认证服务"""

    @classmethod
    async def authenticate_user_service(cls, request: Request, redis: Redis, login_form: CustomOAuth2PasswordRequestForm, db: AsyncSession) -> UserModel:
        """
        用户认证
        
        Args:
            request: 请求对象
            login_form: 登录表单
            db: 数据库会话
            
        Returns:
            UserModel: 认证通过的用户对象
            
        Raises:
            CustomException: 认证失败时抛出异常
        """
        # 判断是否来自API文档
        referer = request.headers.get('referer', '')
        request_from_docs = referer.endswith(('docs', 'redoc'))
        
        # 验证码校验
        if settings.CAPTCHA_ENABLE and not request_from_docs:
            await CaptchaService.check_captcha_service(redis=redis, key=login_form.captcha_key, captcha=login_form.captcha)

        # 用户认证
        auth = AuthSchema(db=db)
        user = await UserCRUD(auth).get_by_username_crud(username=login_form.username)

        if not user:
            raise CustomException(msg="用户不存在")

        if not PwdUtil.verify_password(plain_password=login_form.password, password_hash=user.password):
            logger.warning(f'用户 {login_form.username} 密码错误')
            raise CustomException(msg="密码错误")

        if not user.available:
            raise CustomException(msg="用户已被停用")

        # 更新最后登录时间
        user = await UserCRUD(auth).update_last_login_crud(id=user.id)
        
        # 创建token
        token = await cls.create_token_service(redis=redis, username=user.username)
        user_agent = parse(request.headers.get("user-agent"))
        login_location = await IpLocalUtil.get_ip_location(request.client.host)
        # 缓存中构建在线用户信息
        await RedisCURD(redis).set(
            key=f"{RedisInitKeyConfig.ONLINE_USER.key}:{user.username}",
            value=OnlineOutSchema(
                session_id=token.access_token,
                user_id=user.id, 
                name=user.name,
                user_name=user.username,
                ipaddr=request.client.host,
                login_location=login_location,
                os=user_agent.os.family,
                browser = user_agent.browser.family,
                login_time=user.last_login
            ).model_dump_json(),
            expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        return user

    @classmethod
    async def create_token_service(cls, redis: Redis, username: str) -> JWTOutSchema:
        """
        创建访问令牌和刷新令牌
        
        Args:
            username: 用户名
            request: 请求对象
            
        Returns:
            JWTOutSchema: 包含访问令牌和刷新令牌的响应对象
        """
        access_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        now = datetime.now()
        access_token = create_access_token(payload=JWTPayloadSchema(
            sub=username,
            is_refresh=False,
            exp=now + access_expires,
        ))
        refresh_token = create_access_token(payload=JWTPayloadSchema(
            sub=username,
            is_refresh=True,
            exp=now + refresh_expires,
        ))

        # 清除该用户之前的token
        await RedisCURD(redis).delete(f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{username}')
        await RedisCURD(redis).delete(f'{RedisInitKeyConfig.REFRESH_TOKEN.key}:{username}')
        
        # 设置新的token
        await RedisCURD(redis).set(
            key=f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{username}',
            value=access_token,
            expire=int(access_expires.total_seconds())
        )

        await RedisCURD(redis).set(
            key=f'{RedisInitKeyConfig.REFRESH_TOKEN.key}:{username}',
            value=refresh_token,
            expire=int(refresh_expires.total_seconds())
        )

        return JWTOutSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_expires.total_seconds(),
            token_type=settings.TOKEN_TYPE
        )

    @classmethod
    async def refresh_token_service(cls, redis: Redis, refresh_token: RefreshTokenPayloadSchema) -> JWTOutSchema:
        """
        刷新访问令牌
        
        Args:
            refresh_token: 刷新令牌
            
        Returns:
            JWTOutSchema: 新的令牌对象
            
        Raises:
            CustomException: 刷新令牌无效时抛出异常
        """
        token_payload: JWTPayloadSchema = decode_access_token(refresh_token.refresh_token)
        if not token_payload.is_refresh:
            raise CustomException(msg="非法凭证")

        return await cls.create_token_service(redis=redis, username=token_payload.sub)

    @classmethod
    async def logout_services_service(cls, redis: Redis, token: LogoutPayloadSchema) -> bool:
        """
        退出登录
        
        Args:
            request: 请求对象
            token: 令牌
            
        Returns:
            bool: 退出成功返回True
        """
        payload: JWTPayloadSchema = decode_access_token(token.token)
        username: str = payload.sub
        
        # 删除Redis中的在线用户、访问令牌、刷新令牌
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ONLINE_USER.key}:{username}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.ACCESS_TOKEN.key}:{username}")
        await RedisCURD(redis).delete(f"{RedisInitKeyConfig.REFRESH_TOKEN.key}:{username}")

        logger.info(f"用户退出登录成功,会话账号:{username}")
        return True


class CaptchaService:
    """验证码服务"""

    @classmethod
    async def get_captcha_service(cls, redis: Redis) -> Dict[str, Union[CaptchaKey, CaptchaBase64]]:
        """
        获取验证码
        
        Args:
            request: 请求对象
            
        Returns:
            Dict: 包含验证码key和base64图片的字典
            
        Raises:
            CustomException: 验证码服务未启用时抛出异常
        """
        if not settings.CAPTCHA_ENABLE:
            raise CustomException(msg="未开启验证码服务")

        # 生成验证码图片和值
        captcha_base64, captcha_value = CaptchaUtil.captcha_arithmetic()
        captcha_key = get_random_character()

        # 保存到Redis并设置过期时间
        redis_key = f"{RedisInitKeyConfig.CAPTCHA_CODES.key}:{captcha_key}"
        await RedisCURD(redis).set(
            key=redis_key,
            value=captcha_value,
            expire=settings.CAPTCHA_EXPIRE_SECONDS
        )

        logger.info(f"生成验证码成功,验证码:{captcha_value}")

        # 返回验证码信息
        return CaptchaOutSchema(
            key=CaptchaKey(captcha_key),
            img_base=CaptchaBase64(f"data:image/png;base64,{captcha_base64}")
        ).model_dump()

    @classmethod
    async def check_captcha_service(cls, redis: Redis, key: str, captcha: str) -> bool:
        """
        校验验证码
        
        Args:
            request: 请求对象
            key: 验证码key
            captcha: 用户输入的验证码
            
        Returns:
            bool: 验证通过返回True
            
        Raises:
            CustomException: 验证码无效或错误时抛出异常
        """
        if not captcha:
            raise CustomException(msg="验证码不能为空")

        # 获取Redis中存储的验证码
        redis_key = f'{RedisInitKeyConfig.CAPTCHA_CODES.key}:{key}'
        
        captcha_value = await RedisCURD(redis).get(redis_key)
        if not captcha_value:
            logger.warning('验证码已过期或不存在')
            raise CustomException(msg="验证码已过期")

        # 验证码不区分大小写比对
        if captcha.lower() != captcha_value.lower():
            logger.warning(f'验证码错误,用户输入:{captcha},正确值:{captcha_value}')
            raise CustomException(msg="验证码错误")

        # 验证成功后删除验证码,避免重复使用
        await RedisCURD(redis).delete(redis_key)
        logger.info(f'验证码校验成功,key:{key}')
        return True
