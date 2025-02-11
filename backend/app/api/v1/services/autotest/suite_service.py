# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.suite_schema import SuiteOutSchema, SuiteCreateSchema, SuiteUpdateSchema
from app.api.v1.params.autotest.suite_param import SuiteQueryParams
from app.api.v1.cruds.autotest.suite_crud import SuiteCRUD


class SuiteService:
    """
    套件服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await SuiteCRUD(auth).get_obj_by_id(id=id)
        return SuiteOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: SuiteQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await SuiteCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [SuiteOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: SuiteCreateSchema) -> Dict:
        obj = await SuiteCRUD(auth).create_obj(data=data)
        return SuiteOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: SuiteUpdateSchema) -> Dict:
        obj = await SuiteCRUD(auth).update_obj(id=data.id, data=data)
        return SuiteOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await SuiteCRUD(auth).delete_obj(ids=[id])
