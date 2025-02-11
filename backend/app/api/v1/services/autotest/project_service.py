# -*- coding: utf-8 -*-

from typing import List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.autotest.project_schema import ProjectOutSchema, ProjectCreateSchema, ProjectUpdateSchema
from app.api.v1.params.autotest.project_param import ProjectQueryParams
from app.api.v1.cruds.autotest.project_crud import ProjectCRUD


class ProjectService:
    """
    项目服务层
    """
    
    @classmethod
    async def get_detail_services(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await ProjectCRUD(auth).get_obj_by_id(id=id)
        return ProjectOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_list_services(cls, auth: AuthSchema, search: ProjectQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        obj_list = await ProjectCRUD(auth).get_obj_list(search=search.__dict__, order_by=order_by)
        return [ProjectOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_services(cls, auth: AuthSchema, data: ProjectCreateSchema) -> Dict:
        obj = await ProjectCRUD(auth).create_obj(data=data)
        return ProjectOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_services(cls, auth: AuthSchema, data: ProjectUpdateSchema) -> Dict:
        obj = await ProjectCRUD(auth).update_obj(id=data.id, data=data)
        return ProjectOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_services(cls, auth: AuthSchema, id: int) -> None:
        await ProjectCRUD(auth).delete_obj(ids=[id])
