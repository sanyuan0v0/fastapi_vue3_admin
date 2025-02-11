# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import JSON, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class TaskModel(ModelBase):
    """
    自动化-环境表
    """
    __tablename__ = "auto_tasks"
    __table_args__ = ({'comment': '自动化-执行记录表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')

    test_case_id = Column(Integer, nullable=False, comment="关联的测试用例ID")
    status = Column(String, nullable=False, comment="执行状态")
    logs = Column(JSON, comment="执行日志")
    actual_response = Column(JSON, comment="实际响应（仅API测试）")
    
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
