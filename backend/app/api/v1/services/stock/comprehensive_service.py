# -*- coding: utf-8 -*-

import io
from typing import Any, List, Dict
from fastapi import UploadFile
import pandas as pd

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.stock.comprehensive_schema import ComprehensiveOutSchema, ComprehensiveDetailSchema

from app.api.v1.params.stock.comprehensive_param import ComprehensiveQueryParams
from app.api.v1.cruds.stock.comprehensive_crud import ComprehensiveCRUD




class ComprehensiveService:
    """
    综合选股模块服务层
    """
    @classmethod
    async def get_comprehensive_detail_service(cls, auth: AuthSchema, date: str, code: str) -> Dict:
        """详情"""
        obj = await ComprehensiveCRUD(auth).get_by_date_code_crud(date=date, code=code)
        return ComprehensiveDetailSchema.model_validate(obj).model_dump()

    @classmethod
    async def get_comprehensive_list_service(cls, auth: AuthSchema, search: ComprehensiveQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        """列表查询"""
        if order_by:
            order_by = eval(order_by)
        obj_list = await ComprehensiveCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [ComprehensiveOutSchema.model_validate(obj).model_dump() for obj in obj_list]
