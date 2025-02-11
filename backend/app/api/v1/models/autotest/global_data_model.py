# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import JSON, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class GlobalDataModel(ModelBase):
    """
    配置表 - 用于存储组织架构中的配置信息
    """
    __tablename__ = "auto_global_data"
    __table_args__ = ({'comment': '自动化-全局参数表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')

    name = Column(String, nullable=False, comment="参数名称")
    value = Column(String, nullable=False, comment="参数值")
    project_id = Column(Integer, ForeignKey("auto_projects.id"), comment="所属项目ID")
    
    # 审计字段
    description = Column(Text, nullable=True, comment="备注说明")
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    creator_id = Column(
        Integer, 
        ForeignKey("system_user.id", ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True, 
        index=True, 
        comment="创建人ID"
    )
    creator = relationship(
        "UserModel", 
        foreign_keys=creator_id, 
        lazy="joined",
        post_update=True,
        uselist=False
    )
