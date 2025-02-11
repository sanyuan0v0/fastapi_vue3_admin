# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.models.autotest.global_data_model import GlobalDataModel
from app.api.v1.schemas.autotest.global_data_schema import GlobalDataCreateSchema, GlobalDataUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema


class GlobalDataCRUD(CRUDBase[GlobalDataModel, GlobalDataCreateSchema, GlobalDataUpdateSchema]):

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        self.auth = auth
        super().__init__(model=GlobalDataModel, auth=auth)
    
    async def get_obj_by_id(self, id: int) -> Optional[GlobalDataModel]:
        """获取对象详情"""
        return await self.get(id=id)
    
    async def get_obj_list(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[GlobalDataModel]:
        """获取对象列表"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_obj(self, data: GlobalDataCreateSchema) -> Optional[GlobalDataModel]:
        """创建对象"""
        return await self.create(data=data)
    
    async def update_obj(self, id: int, data: GlobalDataUpdateSchema) -> Optional[GlobalDataModel]:
        """更新对象"""
        return await self.update(id=id, data=data)
    
    async def delete_obj(self, ids: List[int]) -> None:
        """删除对象"""
        return await self.delete(ids=ids)
