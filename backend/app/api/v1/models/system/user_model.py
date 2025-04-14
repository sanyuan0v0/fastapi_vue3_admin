# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from typing import Optional, List

from app.core.base_model import ModelBase


class UserRolesModel(ModelBase):
    """
    用户角色关联表
    """
    __tablename__ = "system_user_roles"
    __table_args__ = ({'comment': '用户角色关联表'})

    user_id = Column(
        Integer, 
        ForeignKey("system_users.id", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True, 
        comment="用户ID", 
        index=True
    )
    role_id = Column(
        Integer, 
        ForeignKey("system_role.id", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True, 
        comment="角色ID", 
        index=True
    )

class UserPositionsModel(ModelBase):
    """
    用户岗位关联表
    """
    __tablename__ = "system_user_positions" 
    __table_args__ = ({'comment': '用户岗位关联表'})

    user_id = Column(
        Integer, 
        ForeignKey("system_users.id", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True, 
        comment="用户ID", 
        index=True
    )
    position_id = Column(
        Integer, 
        ForeignKey("system_position.id", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True, 
        comment="岗位ID", 
        index=True
    )

class UserModel(ModelBase):
    """
    用户表 - 存储系统用户基本信息
    """
    __tablename__ = "system_users"
    __table_args__ = ({'comment': '用户表'})
    
    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    username = Column(String(150), nullable=False, unique=True, comment="用户名/登录账号")
    password = Column(String(128), nullable=False, comment="密码")
    name = Column(String(40), nullable=False, comment="姓名")
    
    # 联系信息
    mobile = Column(String(20), nullable=True, comment="手机号")
    email = Column(String(255), nullable=True, comment="邮箱")
    
    # 个人信息
    gender = Column(String(20), default='1', nullable=False, comment="性别(1:男 2:女 3:未知)")
    avatar = Column(String(255), nullable=True, comment="头像地址", default="https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png")
    
    # 账号状态
    available = Column(Boolean, default=True, nullable=False, comment="是否启用(True:启用 False:禁用)")
    is_superuser = Column(Boolean, default=False, nullable=False, comment="是否为超级管理员")
    last_login = Column(DateTime, nullable=True, comment="最后登录时间")
    
    # 组织信息
    dept_id = Column(
        Integer,
        ForeignKey('system_dept.id', ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True, index=True, comment="部门ID"
    )
    dept = relationship(
        'DeptModel', 
        primaryjoin="UserModel.dept_id == DeptModel.id", 
        lazy="select", 
        uselist=False)
    roles = relationship(
        "RoleModel", 
        secondary=UserRolesModel.__tablename__, 
        lazy="joined", 
        uselist=True)
    positions = relationship(
        "PositionModel", 
        secondary=UserPositionsModel.__tablename__, 
        lazy="joined", 
        uselist=True)
    
    # 审计字段
    description = Column(Text, nullable=True, comment="备注说明")
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    creator_id = Column(
        Integer, 
        ForeignKey("system_users.id", ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True, 
        index=True, 
        comment="创建人ID"
    )
    creator = relationship(
        "UserModel",
        remote_side=[id],
        foreign_keys=[creator_id],
        lazy="selectin",
        uselist=False
    )