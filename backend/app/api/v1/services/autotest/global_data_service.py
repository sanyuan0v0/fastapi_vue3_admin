# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.global_data_schema import GlobalDataOutSchema, GlobalDataCreateSchema, GlobalDataUpdateSchema
from app.api.v1.params.autotest.global_data_param import GlobalDataQueryParams
from app.api.v1.cruds.autotest.global_data_crud import GlobalDataCRUD


class GlobalDataService:
    """
    全局参数服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await GlobalDataCRUD(auth).get_obj_by_id(id=id)
        return GlobalDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: GlobalDataQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await GlobalDataCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [GlobalDataOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: GlobalDataCreateSchema) -> Dict:
        obj = await GlobalDataCRUD(auth).create_obj(data=data)
        return GlobalDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: GlobalDataUpdateSchema) -> Dict:
        obj = await GlobalDataCRUD(auth).update_obj(id=data.id, data=data)
        return GlobalDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await GlobalDataCRUD(auth).delete_obj(ids=[id])
