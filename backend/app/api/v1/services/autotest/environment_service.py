# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.environment_schema import EnvironmentOutSchema, EnvironmentCreateSchema, EnvironmentUpdateSchema
from app.api.v1.params.autotest.environment_param import EnvironmentQueryParams
from app.api.v1.cruds.autotest.environment_crud import EnvironmentCRUD


class EnvironmentService:
    """
    环境服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await EnvironmentCRUD(auth).get_obj_by_id(id=id)
        return EnvironmentOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: EnvironmentQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await EnvironmentCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [EnvironmentOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: EnvironmentCreateSchema) -> Dict:
        obj = await EnvironmentCRUD(auth).create_obj(data=data)
        return EnvironmentOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: EnvironmentUpdateSchema) -> Dict:
        obj = await EnvironmentCRUD(auth).update_obj(id=data.id, data=data)
        return EnvironmentOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await EnvironmentCRUD(auth).delete_obj(ids=[id])
