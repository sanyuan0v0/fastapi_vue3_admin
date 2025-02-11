# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import JSON, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class APICaseModel(ModelBase):
    """
    自动化-接口用例表
    """
    __tablename__ = "auto_api_case"
    __table_args__ = ({'comment': '自动化-接口用例表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')

    name = Column(String, nullable=False, comment="测试用例名称")
    
    url = Column(String, nullable=False, comment="接口地址")
    method = Column(String, nullable=False, comment="请求方法")
    headers = Column(JSON, comment="请求头")
    data_type = Column(String, nullable=False, comment="请求参数类型(params/data/json/file)")
    data = Column(JSON, comment="请求参数")
    
    expected_status_code = Column(Integer, comment="预期状态码")
    expected_msg = Column(String, comment="预期消息")
    expected_response = Column(JSON, comment="预期响应")
    assertions_status_code = Column(String, comment="状态码断言规则(=, !=, >, <, >=, <=, in, not in)")
    assertions_msg = Column(String, comment="消息断言规则(=, !=, >, <, >=, <=, in, not in)")
    assertions_response = Column(String, comment="响应断言规则(=, !=, >, <, >=, <=, in, not in)")
    
    environment_id = Column(Integer, ForeignKey("auto_environments.id"), comment="所属环境ID")
    global_data_id = Column(Integer, ForeignKey("auto_global_data.id"), comment="关联全局数据ID")
    module_id = Column(Integer, ForeignKey("auto_modules.id"), comment="所属模块ID")
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
