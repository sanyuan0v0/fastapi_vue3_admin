# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import TypeVar, Sequence, Generic, Dict, Any, List, Union, Optional
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.orm import selectinload, DeclarativeBase
from sqlalchemy.engine import Result
from sqlalchemy import asc, func, select, delete, Select, desc, update

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.models.system.dept_model import DeptModel
from app.api.v1.models.system.user_model import UserModel
from app.utils.common_util import get_child_id_map, get_child_recursion
from app.core.exceptions import CustomException

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """基础数据查询层"""

    def __init__(self, model: ModelType, auth: AuthSchema) -> None:
        """
        初始化CRUDBase类
        
        Args:
            model: 数据模型
            auth: 认证信息
        """
        self.model = model
        self.auth = auth
        self.db = auth.db
        self.current_user = auth.user
    async def get(self, **kwargs) -> Optional[ModelType]:
        """
        根据条件获取单个对象
        
        Args:
            **kwargs: 查询条件
            
        Returns:
            Optional[ModelType]: 对象实例
            
        Raises:
            CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**kwargs)
            sql = (select(self.model)
                  .where(*conditions)
                  .distinct())
            sql = await self.__filter_permissions(sql)
            result: Result = await self.db.execute(sql)
            obj = result.scalars().unique().first()
            return obj
        except Exception as e:
            raise CustomException(msg=f"获取查询失败: {str(e)}")

    async def list(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[ModelType]:
        """
        根据条件获取对象列表和总数
        
        Args:
            search: 查询条件,格式为 {'id': value, 'name': value}
            order_by: 排序字段,格式为 [{'id': 'asc'}, {'name': 'desc'}]
            
        Returns:
            Sequence[ModelType]: 对象列表
            
        Raises:
            CustomException: 查询失败时抛出异常
        """
        try:
            conditions = await self.__build_conditions(**search) if search else []
            order = order_by or [{'id': 'asc'}]
            sql = (select(self.model)
                  .where(*conditions)
                  .order_by(*self.__order_by(order))
                  .distinct())
            sql = await self.__filter_permissions(sql)
            result: Result = await self.db.execute(sql)
            return result.scalars().unique().all()
        except Exception as e:
            raise CustomException(msg=f"列表查询失败: {str(e)}")

    async def create(self, data: Union[CreateSchemaType, Dict]) -> ModelType:
        """
        创建新对象
        
        Args:
            data: 对象属性
            
        Returns:
            ModelType: 新创建的对象实例
            
        Raises:
            CustomException: 创建失败时抛出异常
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump()
            obj = self.model(**obj_dict)
            
            if hasattr(self.model, "creator") and self.current_user:
                # 设置创建人ID
                obj.creator_id = self.current_user.id
                # 设置创建人对象
                obj.creator = self.current_user
                
            self.db.add(obj)
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        except Exception as e:
            raise CustomException(msg=f"创建失败: {str(e)}")

    async def update(self, id: int, data: Union[UpdateSchemaType, Dict]) -> ModelType:
        """
        更新对象
        
        Args:
            id: 对象ID
            data: 更新的属性及值
            
        Returns:
            ModelType: 更新后的对象实例
            
        Raises:
            CustomException: 更新失败时抛出异常
        """
        try:
            obj_dict = data if isinstance(data, dict) else data.model_dump(exclude_unset=True, exclude={"id"})
            obj = await self.get(id=id)
            
            for key, value in obj_dict.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
                    
            await self.db.flush()
            await self.db.refresh(obj)
            return obj
        except Exception as e:
            raise CustomException(msg=f"更新失败: {str(e)}")

    async def delete(self, ids: List[int]) -> None:
        """
        删除对象
        
        Args:
            ids: 对象ID列表
            
        Raises:
            CustomException: 删除失败时抛出异常
        """
        try:
            sql = delete(self.model).where(self.model.id.in_(ids))
            sql = await self.__filter_permissions(sql)
            await self.db.execute(sql)
            await self.db.flush()
        except Exception as e:
            raise CustomException(msg=f"删除失败: {str(e)}")

    async def set(self, ids: List[int], **kwargs) -> None:
        """
        批量更新对象
        
        Args:
            ids: 对象ID列表
            **kwargs: 更新的属性及值
            
        Raises:
            CustomException: 更新失败时抛出异常
        """
        try:
            sql = update(self.model).where(self.model.id.in_(ids)).values(**kwargs)
            await self.db.execute(sql)
            await self.db.flush()
        except Exception as e:
            raise CustomException(msg=f"批量更新失败: {str(e)}")

    async def update_relationships(self, objs_to_update: List[ModelType], relationship_field: str, related_objs: List[ModelType]) -> None:
        """
        更新对象关系
        
        Args:
            objs_to_update: 需要更新关系的对象列表
            relationship_field: 关系字段名称
            related_objs: 关联对象列表
            
        Raises:
            CustomException: 更新关系失败时抛出异常
        """
        try:
            for obj in objs_to_update:
                relationship = getattr(obj, relationship_field)
                relationship.clear()
                relationship.extend(related_objs)
            await self.db.flush()
        except Exception as e:
            raise CustomException(msg=f"更新关系失败: {str(e)}")

    async def __filter_permissions(self, sql: Select[Any]) -> Select[Any]:
        """过滤数据权限"""
        if not hasattr(self.model, "creator"):
            return sql
        
        sql = sql.options(selectinload(self.model.creator))
        
        if not self.current_user or self.current_user.is_superuser:
            return sql
        
        if not self.current_user.dept_id or not self.current_user.roles:
            return sql.where(self.model.creator_id == self.current_user.id)
        
        data_scopes = {role.data_scope for role in self.current_user.roles}
        dept_ids = {dept.id for role in self.current_user.roles for dept in role.depts}
        
        if 1 in data_scopes:
            return sql.where(self.model.creator_id == self.current_user.id)
        if 4 in data_scopes:
            return sql
        if 2 in data_scopes:
            dept_ids.add(self.current_user.dept_id)
        if 3 in data_scopes:
            dept_objs = await CRUDBase(DeptModel, self.auth).list()
            id_map = get_child_id_map(dept_objs)
            dept_child_ids = get_child_recursion(id=self.current_user.dept_id, id_map=id_map)
            dept_ids.update(dept_child_ids)

        return sql.where(self.model.creator.has(UserModel.dept_id.in_(list(dept_ids))))

    def __order_by(self, order_by: List[Dict[str, str]]) -> List[ColumnElement]:
        """
        获取排序字段
        
        Args:
            order_by: 排序字段列表,格式为 [{'id': 'asc'}, {'name': 'desc'}]
            
        Returns:
            List[ColumnElement]: 排序字段列表
        """
        columns = []
        for order in order_by:
            for field, direction in order.items():
                column = getattr(self.model, field)
                columns.append(desc(column) if direction.lower() == 'desc' else asc(column))
        return columns

    async def __build_conditions(self, **kwargs) -> List[ColumnElement]:
        """
        构建查询条件
        
        Args:
            **kwargs: 查询参数
            
        Returns:
            List[ColumnElement]: SQL条件表达式列表
        """
        conditions = []
        for key, value in kwargs.items():
            if value is None or value == "":
                continue

            attr = getattr(self.model, key)
            if isinstance(value, tuple):
                seq, val = value
                if seq == "None":
                    conditions.append(attr.is_(None))
                elif seq == "not None":
                    conditions.append(attr.isnot(None))
                elif seq == "date" and val:
                    conditions.append(func.date_format(attr, "%Y-%m-%d") == val)
                elif seq == "month" and val:
                    conditions.append(func.date_format(attr, "%Y-%m") == val)
                elif seq == "like" and val:
                    conditions.append(attr.like(f"%{val}%"))
                elif seq == "in" and val:
                    conditions.append(attr.in_(val))
                elif seq == "between" and isinstance(val, (list, tuple)) and len(val) == 2:
                    conditions.append(attr.between(val[0], val[1]))
                elif seq == "!=" and val:
                    conditions.append(attr != val)
                elif seq in [">", ">=", "<=", "=="] and val:
                    conditions.append(getattr(attr, seq.replace("==", "__eq__"))(val))
            else:
                conditions.append(attr == value)
        return conditions
