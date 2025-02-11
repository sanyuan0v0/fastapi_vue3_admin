# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.repont_schema import ReportOutSchema, ReportCreateSchema, ReportUpdateSchema
from app.api.v1.params.autotest.repont_param import ReportQueryParams
from app.api.v1.cruds.autotest.repont_crud import ReportCRUD


class ReportService:
    """
    报告服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await ReportCRUD(auth).get_obj_by_id(id=id)
        return ReportOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: ReportQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await ReportCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [ReportOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: ReportCreateSchema) -> Dict:
        obj = await ReportCRUD(auth).create_obj(data=data)
        return ReportOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: ReportUpdateSchema) -> Dict:
        obj = await ReportCRUD(auth).update_obj(id=data.id, data=data)
        return ReportOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await ReportCRUD(auth).delete_obj(ids=[id])

