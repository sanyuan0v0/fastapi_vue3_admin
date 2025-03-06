# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.cruds.system.menu_crud import MenuCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.menu_schema import (
    MenuCreateSchema,
    MenuUpdateSchema,
    MenuOutSchema
)
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.common_util import (
    get_parent_id_map,
    get_parent_recursion,
    get_child_id_map,
    get_child_recursion
)
from app.api.v1.params.system.menu_param import MenuQueryParams


class MenuService:
    """
    菜单模块服务层
    """

    @classmethod
    async def get_menu_detail(cls, auth: AuthSchema, id: int) -> Dict:
        menu = await MenuCRUD(auth).get_menu_by_id(id=id)
        menu_dict = MenuOutSchema.model_validate(menu).model_dump()
        return menu_dict

    @classmethod
    async def get_menu_list(cls, auth: AuthSchema, search: MenuQueryParams, order_by: List[Dict] = None) -> List[Dict]:
        order_by = order_by if order_by else [{"order": "asc"}]
        menu_list = await MenuCRUD(auth).get_menu_list(search=search.__dict__, order_by=order_by)
        menu_dict_list = [MenuOutSchema.model_validate(menu).model_dump() for menu in menu_list]
        return menu_dict_list

    @classmethod
    async def create_menu(cls, auth: AuthSchema, data: MenuCreateSchema) -> Dict:
        menu = await MenuCRUD(auth).get(name=data.name)
        if menu:
            raise CustomException(msg='创建失败，该菜单已存在')
        if data.parent_id:
            parent_menu = await MenuCRUD(auth).get_menu_by_id(id=data.parent_id)
            data.parent_name = parent_menu.name
        new_menu = await MenuCRUD(auth).create(data=data)
        new_menu_dict = MenuOutSchema.model_validate(new_menu).model_dump()
        return new_menu_dict

    @classmethod
    async def update_menu(cls, auth: AuthSchema, data: MenuUpdateSchema) -> Dict:
        menu = await MenuCRUD(auth).get_menu_by_id(id=data.id)
        if not menu:
            raise CustomException(msg='更新失败，该菜单不存在')
        exist_menu = await MenuCRUD(auth).get(name=data.name)
        if exist_menu and exist_menu.id != data.id:
            raise CustomException(msg='更新失败，菜单名称重复')
        
        if data.parent_id:
            parent_menu = await MenuCRUD(auth).get_menu_by_id(id=data.parent_id)
            data.parent_name = parent_menu.name
        new_menu = await MenuCRUD(auth).update(id=data.id, data=data)
        
        await cls.set_menu_available(auth=auth, data=BatchSetAvailable(ids=[data.id], available=data.available))
        
        new_menu_dict = MenuOutSchema.model_validate(new_menu).model_dump()
        return new_menu_dict
    
    @classmethod
    async def delete_menu(cls, auth: AuthSchema, id: int) -> None:
        menu = await MenuCRUD(auth).get_menu_by_id(id=id)
        if not menu:
            raise CustomException(msg='删除失败，该菜单不存在')
        await MenuCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_menu_available(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        递归获取所有父、子级菜单，然后批量修改菜单可用状态
        """
        menu_list = await MenuCRUD(auth).get_menu_list()
        total_ids = []
        
        if data.available:
            # 激活，则需要把所有父级菜单都激活
            id_map = get_parent_id_map(model_list=menu_list)
            for menu_id in data.ids:
                enable_ids = get_parent_recursion(id=menu_id, id_map=id_map)
                total_ids.extend(enable_ids)
        else:
            # 禁止，则需要把所有子级菜单都禁止
            id_map = get_child_id_map(model_list=menu_list)
            for menu_id in data.ids:
                disable_ids = get_child_recursion(id=menu_id, id_map=id_map)
                total_ids.extend(disable_ids)

        await MenuCRUD(auth).set_menu_available(ids=total_ids, available=data.available)
