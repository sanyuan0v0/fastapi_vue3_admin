# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.models.demo.example_model import ExampleModel
from app.api.v1.schemas.demo.example_schema import ExampleCreateSchema, ExampleUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema


class ExampleCRUD(CRUDBase[ExampleModel, ExampleCreateSchema, ExampleUpdateSchema]):
    """示例数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        self.auth = auth
        super().__init__(model=ExampleModel, auth=auth)

    async def get_by_id_crud(self, id: int) -> Optional[ExampleModel]:
        """详情"""
        return await self.get(id=id)
    
    async def get_list_crud(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[ExampleModel]:
        """列表查询"""
        return await self.list(search=search, order_by=order_by)
    
    async def create_crud(self, data: ExampleCreateSchema) -> Optional[ExampleModel]:
        """创建"""
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: ExampleUpdateSchema) -> Optional[ExampleModel]:
        """更新"""
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """删除"""
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """批量设置可用状态"""
        return await self.set(ids=ids, status=status)