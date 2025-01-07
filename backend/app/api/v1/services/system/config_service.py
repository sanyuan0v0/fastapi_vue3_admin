# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.config_schema import ConfigCreateSchema, ConfigUpdateSchema, ConfigOutSchema
from app.api.v1.params.system.config_param import ConfigQueryParams
from app.api.v1.cruds.system.config_crud import ConfigCRUD


class ConfigService:
    """
    配置管理模块服务层
    """
    
    @classmethod
    async def detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        config_obj = await ConfigCRUD(auth).get_curd(id=id)
        return ConfigOutSchema.model_validate(config_obj).model_dump()
    
    @classmethod
    async def list_services(cls, auth: AuthSchema, search: ConfigQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        config_obj_list = await ConfigCRUD(auth).list_curd(search=search.__dict__, order_by=order_by)
        return [ConfigOutSchema.model_validate(config_obj).model_dump() for config_obj in config_obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: ConfigCreateSchema) -> Dict:
        config_obj = await ConfigCRUD(auth).create_curd(data=data)
        return ConfigOutSchema.model_validate(config_obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, id: int, data: ConfigUpdateSchema) -> Dict:
        config_obj = await ConfigCRUD(auth).update_curd(id=id, data=data)
        return ConfigOutSchema.model_validate(config_obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await ConfigCRUD(auth).delete_curd(ids=[id])

