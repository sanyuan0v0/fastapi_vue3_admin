# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import JSON, Boolean, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class CaseModel(ModelBase):
    """
    自动化-用例表
    """
    __tablename__ = "auto_cases"
    __table_args__ = ({'comment': '自动化-用例表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')

    name = Column(String, nullable=False, comment="测试用例名称")
    status = Column(Boolean, default=True, comment="是否启用")
    url = Column(String, nullable=False, comment="接口地址")
    method = Column(String, nullable=False, comment="请求方法")
    headers = Column(JSON, comment="请求头")
    params = Column(JSON, comment="Query参数")
    body = Column(JSON, comment="请求体")
    files = Column(JSON, comment="上传文件配置")
    parameter_need = Column(Boolean, default=True, comment="是否需要公共参数")
    
    # 预期结果
    expected = Column(JSON, comment="断言配置,格式:[{type:'status_code',rule:'equals',expect:200},{type:'msg',rule:'contains',expect:'success'},{type:'response',rule:'jsonpath',expect:'$.code'}]")
    

    project_id = Column(Integer, ForeignKey("auto_projects.id", ondelete="CASCADE"), nullable=False, comment="所属项目ID")
    project = relationship("ProjectModel", foreign_keys=project_id, lazy="joined", uselist=False)

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
