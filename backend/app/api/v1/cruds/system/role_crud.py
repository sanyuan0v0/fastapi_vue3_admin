# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence, Optional

from app.core.base_crud import CRUDBase
from app.api.v1.models.system.role_model import RoleModel
from app.api.v1.schemas.system.role_schema import RoleCreateSchema, RoleUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.cruds.system.menu_crud import MenuCRUD
from app.api.v1.cruds.system.dept_crud import DeptCRUD


class RoleCRUD(CRUDBase[RoleModel, RoleCreateSchema, RoleUpdateSchema]):
    """角色模块数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        self.auth = auth
        super().__init__(model=RoleModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[RoleModel]:
        """根据id获取角色信息"""
        return await self.get(id=id)

    async def get_list_crud(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[RoleModel]:
        """获取角色列表"""
        return await self.list(search=search, order_by=order_by)

    async def set_role_menus_crud(self, role_ids: List[int], menu_ids: List[int]) -> None:
        """设置角色的菜单权限"""
        roles = await self.list(search={"id": ("in", role_ids)})
        menus = await MenuCRUD(self.auth).get_list_crud(search={"id": ("in", menu_ids)})
        await self.update_relationships(
            objs_to_update=roles,
            relationship_field="menus",
            related_objs=menus
        )

    async def set_role_data_scope_crud(self, role_ids: List[int], data_scope: int) -> None:
        """设置角色的数据范围"""
        await self.set(ids=role_ids, data_scope=data_scope)

    async def set_role_depts_crud(self, role_ids: List[int], dept_ids: List[int]) -> None:
        """设置角色的部门权限"""
        roles = await self.list(search={"id": ("in", role_ids)})
        depts = await DeptCRUD(self.auth).get_list_crud(search={"id": ("in", dept_ids)})
        await self.update_relationships(
            objs_to_update=roles,
            relationship_field="depts",
            related_objs=depts
        )

    async def set_available_crud(self, ids: List[int], available: bool) -> None:
        """设置角色的可用状态"""
        await self.set(ids=ids, available=available)
