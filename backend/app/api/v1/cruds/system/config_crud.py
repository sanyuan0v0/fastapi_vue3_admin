# -*- coding: utf-8 -*-

from typing import Dict, List, Optional, Sequence

from app.core.base_crud import CRUDBase
from app.api.v1.models.system.config_model import ConfigModel
from app.api.v1.schemas.system.config_schema import ConfigCreateSchema,ConfigUpdateSchema
from app.api.v1.schemas.system.auth_schema import AuthSchema


class ConfigCRUD(CRUDBase[ConfigModel, ConfigCreateSchema, ConfigUpdateSchema]):
    """操作配置数据层"""

    def __init__(self, auth: AuthSchema) -> None:
        """初始化配置CRUD"""
        self.auth = auth
        super().__init__(model=ConfigModel, auth=auth)
    
    async def get_crud(self, id: int) -> Optional[ConfigModel]:
        """获取配置"""
        return await self.get(id=id)

    async def update_crud(self, id: int, data: ConfigUpdateSchema) -> Optional[ConfigModel]:
        """更新配置"""
        return await self.update(id=id, data=data)
