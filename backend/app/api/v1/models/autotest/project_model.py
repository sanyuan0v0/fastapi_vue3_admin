# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class ProjectModel(ModelBase):
    """
    自动化测试项目表
    """
    __tablename__ = "auto_projects"
    __table_args__ = ({'comment': '自动化测试项目表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')

    name = Column(String, nullable=False, comment="项目名称")
    base_url = Column(String, nullable=False, comment="基础URL")
    headers = Column(JSON, nullable=False, comment="公共请求头")
    message = Column(JSON, nullable=False, comment="通知配置")
    

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

    cases = relationship("CaseModel", back_populates="project")
    tasks = relationship("TaskModel", back_populates="project")
