# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import JSON, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class ReportModel(ModelBase):
    """
    自动化-环境表
    """
    __tablename__ = "auto_report"
    __table_args__ = ({'comment': '自动化-测试报告表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')

    name = Column(String(40), nullable=False, default="名称", comment="名称")
    task_id = Column(Integer, nullable=False, comment="关联的任务ID")
    summary = Column(JSON, comment="报告摘要")
    details = Column(JSON, comment="详细报告")
    
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
