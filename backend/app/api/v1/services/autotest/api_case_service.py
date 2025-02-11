# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.api_case_schema import APICaseOutSchema, APICaseCreateSchema, APICaseUpdateSchema
from app.api.v1.params.autotest.api_case_param import APICaseQueryParams
from app.api.v1.cruds.autotest.api_case_crud import APICaseCRUD


class APICaseService:
    """
    接口用例服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await APICaseCRUD(auth).get_obj_by_id(id=id)
        return APICaseOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: APICaseQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await APICaseCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [APICaseOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: APICaseCreateSchema) -> Dict:
        obj = await APICaseCRUD(auth).create_obj(data=data)
        return APICaseOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: APICaseUpdateSchema) -> Dict:
        obj = await APICaseCRUD(auth).update_obj(id=data.id, data=data)
        return APICaseOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await APICaseCRUD(auth).delete_obj(ids=[id])
