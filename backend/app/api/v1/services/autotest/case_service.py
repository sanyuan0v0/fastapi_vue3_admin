# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.case_schema import CaseOutSchema, CaseCreateSchema, CaseCreateSchema
from app.api.v1.params.autotest.case_param import CaseQueryParams
from app.api.v1.cruds.autotest.case_crud import CaseCRUD


class CaseService:
    """
    接口用例服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await CaseCRUD(auth).get_obj_by_id(id=id)
        return CaseOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: CaseQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await CaseCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [CaseOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: CaseCreateSchema) -> Dict:
        obj = await CaseCRUD(auth).create_obj(data=data)
        return CaseOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: CaseCreateSchema) -> Dict:
        obj = await CaseCRUD(auth).update_obj(id=data.id, data=data)
        return CaseOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await CaseCRUD(auth).delete_obj(ids=[id])
