# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.module_schema import ModuleOutSchema, ModuleCreateSchema, ModuleUpdateSchema
from app.api.v1.params.autotest.module_param import ModuleQueryParams
from app.api.v1.cruds.autotest.module_crud import ModuleCRUD


class ModuleService:
    """
    模块服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await ModuleCRUD(auth).get_obj_by_id(id=id)
        return ModuleOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: ModuleQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await ModuleCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [ModuleOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: ModuleCreateSchema) -> Dict:
        obj = await ModuleCRUD(auth).create_obj(data=data)
        return ModuleOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: ModuleUpdateSchema) -> Dict:
        obj = await ModuleCRUD(auth).update_obj(id=data.id, data=data)
        return ModuleOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await ModuleCRUD(auth).delete_obj(ids=[id])
