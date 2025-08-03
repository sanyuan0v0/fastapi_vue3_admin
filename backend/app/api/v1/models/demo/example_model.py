# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class ExampleModel(ModelBase):
    """
    示例表
    """

    __tablename__ = 'demo_example'
    __table_args__ = ({'comment': '示例表'})

    id=Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    name=Column(String(64), nullable=True, default='', comment='名称')
    description=Column(Text, nullable=True, comment='描述')
    status = Column(Boolean, default=False, nullable=True, comment='任务状态:正常,停止')
    
    # 审计字段
    description = Column(Text, nullable=True, comment="备注说明")
    created_at = Column(DateTime, nullable=True, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    creator_id = Column(
        Integer, 
        ForeignKey("system_users.id", ondelete="SET NULL", onupdate="CASCADE"), 
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

