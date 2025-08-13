# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.models.stock.comprehensive_model import ComprehensiveModel
from app.api.v1.schemas.stock.comprehensive_schema import ComprehensiveCreateSchema, ComprehensiveUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema


class ComprehensiveCRUD(CRUDBase[ComprehensiveModel, ComprehensiveCreateSchema, ComprehensiveUpdateSchema]):
    """综合选股数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化CRUD"""
        self.auth = auth
        super().__init__(model=ComprehensiveModel, auth=auth)

    async def get_by_date_code_crud(self, date: str, code: str) -> Optional[ComprehensiveModel]:
        """详情"""
        return await self.get(date=date, code=code)
    
    async def get_list_crud(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[ComprehensiveModel]:
        """列表查询"""
        order_by = order_by or [{"date": 'desc'}]
        return await self.list(search=search, order_by=order_by)
    
    async def create_crud(self, data: ComprehensiveCreateSchema) -> Optional[ComprehensiveModel]:
        """创建"""
        return await self.create(data=data)
    
    async def update_crud(self, id: int, data: ComprehensiveUpdateSchema) -> Optional[ComprehensiveModel]:
        """更新"""
        return await self.update(id=id, data=data)
    
    async def delete_crud(self, ids: List[int]) -> None:
        """删除"""
        return await self.delete(ids=ids)
    
    async def set_available_crud(self, ids: List[int], status: bool) -> None:
        """批量设置可用状态"""
        return await self.set(ids=ids, status=status)