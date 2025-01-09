# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.models.system.config_model import ConfigModel
from app.api.v1.schemas.system.config_schema import ConfigCreateSchema,ConfigUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema


class ConfigCRUD(CRUDBase[ConfigModel, ConfigCreateSchema, ConfigUpdateSchema]):
    """操作配置数据查询层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化配置CRUD"""
        self.auth = auth
        super().__init__(model=ConfigModel, auth=auth)
    
    async def list_curd(self, search: Dict = None, order_by: List[Dict[str, str]] = None) -> Sequence[ConfigModel]:
        """获取配置列表"""
        return await self.list(search=search, order_by=order_by)
    
    async def update_curd(self, id: int, data: ConfigUpdateSchema) -> Optional[ConfigModel]:
        """更新配置"""
        return await self.update(id=id, data=data)
