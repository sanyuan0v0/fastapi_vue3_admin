# -*- coding: utf-8 -*-

import io
from typing import Any, List, Dict
from fastapi import UploadFile
import pandas as pd

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.stock.spot_schema import SpotOutSchema, SpotDetailSchema

from app.api.v1.params.stock.spot_param import SpotQueryParams
from app.api.v1.cruds.stock.spot_crud import SpotCRUD




class SpotService:
    """
    每日股票数据模块服务层
    """
    @classmethod
    async def get_spot_detail_service(cls, auth: AuthSchema, date: str, code: str) -> Dict:
        """详情"""
        obj = await SpotCRUD(auth).get_by_date_code_crud(date=date, code=code)
        return SpotDetailSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_spot_list_service(cls, auth: AuthSchema, search: SpotQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        """列表查询"""
        if order_by:
            order_by = eval(order_by)
        obj_list = await SpotCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [SpotOutSchema.model_validate(obj).model_dump() for obj in obj_list]
