# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.notification_config_schema import NotificationConfigOutSchema, NotificationConfigCreateSchema, NotificationConfigUpdateSchema
from app.api.v1.params.autotest.notification_config_param import NotificationConfigQueryParams
from app.api.v1.cruds.autotest.notification_config_crud import NotificationConfigCRUD


class NotificationConfigService:
    """
    通知配置服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await NotificationConfigCRUD(auth).get_obj_by_id(id=id)
        return NotificationConfigOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: NotificationConfigQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await NotificationConfigCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [NotificationConfigOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: NotificationConfigCreateSchema) -> Dict:
        obj = await NotificationConfigCRUD(auth).create_obj(data=data)
        return NotificationConfigOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: NotificationConfigUpdateSchema) -> Dict:
        obj = await NotificationConfigCRUD(auth).update_obj(id=data.id, data=data)
        return NotificationConfigOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await NotificationConfigCRUD(auth).delete_obj(ids=[id])

