# -*- coding: utf-8 -*-

from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Optional
from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends

from app.core.exceptions import CustomException
from app.core.security import OAuth2Schema, decode_access_token
from app.core.database import session_connect
from app.core.logger import logger
from app.api.v1.cruds.system.user_crud import UserCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema


async def db_getter() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话连接"""
    async with session_connect() as session:
        async with session.begin():
            yield session

async def redis_getter(request: Request) -> Redis:
    """获取Redis连接"""
    return request.app.state.redis

async def mongo_getter(request: Request) -> AsyncIOMotorDatabase:
    """获取MongoDB连接"""
    return request.app.state.mongo

async def get_current_user(
    request: Request,
    token: str = Depends(OAuth2Schema),
    db: AsyncSession = Depends(db_getter)
) -> AuthSchema:
    """
    获取并验证当前用户信息
    
    Args:
        request: 请求对象
        token: 认证token
        db: 数据库会话
        
    Returns:
        AuthSchema: 包含用户信息的认证对象
        
    Raises:
        CustomException: 认证失败时抛出异常
    """
    # 处理Bearer token
    if token.startswith('Bearer'):
        token = token.split(' ')[1]
        
    # 解析token
    payload = decode_access_token(token)
    if not payload or not hasattr(payload, 'is_refresh') or payload.is_refresh:
        raise CustomException(msg="非法凭证", status_code=401)
        
    username = payload.sub
        
    auth = AuthSchema(db=db)
    
    # 获取用户信息
    user = await UserCRUD(auth).get_by_username_crud(username=username)
    if not user:
        raise CustomException(msg="用户不存在")
    if not user.available:
        raise CustomException(msg="用户已被停用")
    
    # 设置请求上下文
    request.scope["user_id"] = user.id
    request.scope["user_username"] = user.username
    
    # 过滤可用的角色和职位
    if hasattr(user, 'roles'):
        user.roles = [role for role in user.roles if role.available]
    if hasattr(user, 'positions'):
        user.positions = [pos for pos in user.positions if pos.available]

    auth.user = user
    return auth


class AuthPermission:
    """权限验证类"""
    
    def __init__(self, permissions: Optional[list[str]] = None, check_data_scope: bool = True) -> None:
        """
        初始化权限验证
        
        Args:
            permissions: 权限标识列表
            check_data_scope: 是否启用严格模式校验
        """
        self.permissions = set(permissions) if permissions else None
        self.check_data_scope = check_data_scope

    async def __call__(
            self,
            auth: AuthSchema = Depends(get_current_user),
    ) -> AuthSchema:
        """
        执行权限验证
        
        Args:
            request: 请求对象
            auth: 认证信息
            
        Returns:
            AuthSchema: 认证对象
            
        Raises:
            CustomException: 权限验证失败时抛出异常
        """
        auth.check_data_scope = self.check_data_scope

        # 超级管理员直接通过
        if auth.user.is_superuser:
            return auth

        # 无需验证权限
        if not self.permissions:
            return auth

        # 超级管理员权限标识
        if {"*:*:*"} <= self.permissions:
            return auth

        # 获取用户权限集合
        user_permissions = {
            menu.permission 
            for role in auth.user.roles 
            for menu in role.menus 
            if menu.permission and menu.available
        }

        # 权限验证
        if self.check_data_scope:
            # 严格模式:要求所有权限都满足
            if not all(perm in user_permissions for perm in self.permissions):
                logger.error(f"用户 {auth.user.name} 缺少所需的权限: {self.permissions}")
                raise CustomException(msg="无权限操作", status_code=403)
        else:
            # 非严格模式:满足任一权限即可
            if not any(perm in user_permissions for perm in self.permissions):
                logger.error(f"用户 {auth.user.name} 缺少任何所需的权限: {self.permissions}")
                raise CustomException(msg="无权限操作", status_code=403)

        return auth
