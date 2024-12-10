# -*- coding: utf-8 -*-

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class ModelBase(AsyncAttrs, DeclarativeBase):
    """
    SQLAlchemy 基础模型类
    继承自 AsyncAttrs 和 DeclarativeBase,提供异步操作支持
    """
    __abstract__ = True  # 声明为抽象基类,不会创建实际数据库表
