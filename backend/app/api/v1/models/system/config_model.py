# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
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

    title = Column(String(40), nullable=False, default="FastAPI Vue Admin", comment="网站标题")
    favicon = Column(String(100), nullable=False, default="http://localhost:8000/api/v1/static/upload/image/png/2025/01/09/logo_20250109090456A114.png", comment="网站favicon")
    logo = Column(String(100), nullable=False, default="http://localhost:8000/api/v1/static/upload/image/png/2025/01/09/logo_20250109090448A263.png", comment="网站logo")
    background = Column(String(100), nullable=False, default="http://localhost:8000/api/v1/static/upload/image/png/2025/01/09/background_20250109090435A357.png", comment="网站背景")
    copyright = Column(String(100), nullable=False, default="Copyright © 2021-2025 fastapi-vue-admin.com 版权所有", comment="版权信息")
    keep_record = Column(String(100), nullable=False, default="晋ICP备18005113号-3", comment="备案信息")
    help_url = Column(String(100), nullable=False, default="https://django-vue-admin.com", comment="帮助链接")
    privacy_url = Column(String(100), nullable=False, default="https://gitee.com/tao__tao/fastapi_vue3_admin/blob/main/docs/clause/privacy.md", comment="隐私政策链接")
    clause_url = Column(String(100), nullable=False, default="https://gitee.com/tao__tao/fastapi_vue3_admin/blob/main/docs/clause/terms_service.md", comment="服务条款链接")
    code_url = Column(String(100), nullable=False, default="https://gitee.com/tao__tao/fastapi_vue3_admin.git", comment="源码地址")

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
