# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Text, DateTime, JSON
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class ConfigModel(ModelBase):
    """
    配置表 - 用于存储组织架构中的配置信息
    """
    __tablename__ = "system_config"
    __table_args__ = ({'comment': '配置表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, comment='主键ID')
    name = Column(String(40), nullable=False, comment="配置名称", unique=True)
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    fied_key = Column(String(100), nullable=False, comment="键", unique=True)
    fied_value = Column(Text, nullable=True, comment="值")

    # 层级关系
    parent_id = Column(
        Integer, 
        ForeignKey("system_config.id", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=True, 
        index=True, 
        comment="父级配置ID"
    )
    parent = relationship(
        "ConfigModel", 
        cascade='all, delete-orphan', 
        uselist=False
    )
