# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.api.v1.cruds.system.role_crud import RoleCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.role_schema import (
    RoleCreateSchema,
    RoleUpdateSchema,
    RolePermissionSettingSchema,
    RoleOutSchema
)
from app.utils.excel_util import ExcelUtil
from app.api.v1.params.system.role_param import RoleQueryParams


class RoleService:
    """角色模块服务层"""

    @classmethod
    async def get_role_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """获取角色详情"""
        role = await RoleCRUD(auth).get_by_id_crud(id=id)
        return RoleOutSchema.model_validate(role).model_dump()

    @classmethod
    async def get_role_list_service(cls, auth: AuthSchema, search: RoleQueryParams, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        """获取角色列表"""
        if order_by:
            order_by = eval(order_by)
        else:
            order_by = [{"order": "asc"}]
        role_list = await RoleCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [RoleOutSchema.model_validate(role).model_dump() for role in role_list]

    @classmethod
    async def create_role_service(cls, auth: AuthSchema, data: RoleCreateSchema) -> Dict:
        """创建角色"""
        role = await RoleCRUD(auth).get(name=data.name)
        if role:
            raise CustomException(msg='创建失败，该角色已存在')
        new_role = await RoleCRUD(auth).create(data=data)
        return RoleOutSchema.model_validate(new_role).model_dump()

    @classmethod
    async def update_role_service(cls, auth: AuthSchema, data: RoleUpdateSchema) -> Dict:
        """更新角色"""
        role = await RoleCRUD(auth).get_by_id_crud(id=data.id)
        if not role:
            raise CustomException(msg='更新失败，该角色不存在')
        exist_role = await RoleCRUD(auth).get(name=data.name)
        if exist_role and exist_role.id != data.id:
            raise CustomException(msg='更新失败，角色名称重复')
        updated_role = await RoleCRUD(auth).update(id=data.id, data=data)
        return RoleOutSchema.model_validate(updated_role).model_dump()

    @classmethod
    async def delete_role_service(cls, auth: AuthSchema, id: int) -> None:
        """删除角色"""
        role = await RoleCRUD(auth).get_by_id_crud(id=id)
        if not role:
            raise CustomException(msg='删除失败，该角色不存在')
        await RoleCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_role_permission_service(cls, auth: AuthSchema, data: RolePermissionSettingSchema) -> None:
        """设置角色权限"""
        # 设置角色菜单权限
        await RoleCRUD(auth).set_role_menus_crud(role_ids=data.role_ids, menu_ids=data.menu_ids)
        
        # 设置数据权限范围
        await RoleCRUD(auth).set_role_data_scope_crud(role_ids=data.role_ids, data_scope=data.data_scope)
        
        # 设置自定义数据权限部门
        if data.data_scope == 5 and data.dept_ids:
            await RoleCRUD(auth).set_role_depts_crud(role_ids=data.role_ids, dept_ids=data.dept_ids)
        else:
            await RoleCRUD(auth).set_role_depts_crud(role_ids=data.role_ids, dept_ids=[])

    @classmethod
    async def set_role_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """设置角色可用状态"""
        await RoleCRUD(auth).set_available_crud(ids=data.ids, available=data.available)

    @classmethod
    async def export_role_list_service(cls, role_list: List[Dict[str, Any]]) -> bytes:
        """导出角色列表"""
        # 字段映射配置
        mapping_dict = {
            'id': '角色编号',
            'name': '角色名称',
            'order': '显示顺序', 
            'data_scope': '数据权限',
            'available': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 数据权限映射
        data_scope_map = {
            1: '仅本人数据权限',
            2: '本部门数据权限',
            3: '本部门及以下数据权限',
            4: '全部数据权限',
            5: '自定义数据权限'
        }

        # 处理数据
        data = role_list.copy()
        for item in data:
            item['available'] = '正常' if item.get('available') else '停用'
            item['data_scope'] = data_scope_map.get(item.get('data_scope'))

        return ExcelUtil.export_list2excel(list_data=role_list, mapping_dict=mapping_dict)
        