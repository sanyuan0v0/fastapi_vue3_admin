# -*- coding: utf-8 -*-

from typing import Any, Dict, List

from app.api.v1.cruds.system.position_crud import PositionCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.position_schema import (
    PositionCreateSchema,
    PositionUpdateSchema,
    PositionOutSchema,
)
from app.core.base_schema import BatchSetAvailable
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.api.v1.params.system.position_param import PositionQueryParams

class PositionService:
    """岗位模块服务层"""

    @classmethod
    async def get_position_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """获取岗位详情"""
        position = await PositionCRUD(auth).get_by_id_crud(id=id)
        return PositionOutSchema.model_validate(position).model_dump()

    @classmethod
    async def get_position_list_service(cls, auth: AuthSchema, search: PositionQueryParams, order_by: List[Dict] = None) -> List[Dict]:
        """获取岗位列表"""
        if order_by:
            order_by = eval(order_by)
        else:
            order_by = [{"order": "asc"}]
        position_list = await PositionCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [PositionOutSchema.model_validate(position).model_dump() for position in position_list]

    @classmethod
    async def create_position_service(cls, auth: AuthSchema, data: PositionCreateSchema) -> Dict:
        """创建岗位"""
        position = await PositionCRUD(auth).get(name=data.name)
        if position:
            raise CustomException(msg='创建失败，该岗位已存在')
        new_position = await PositionCRUD(auth).create(data=data)
        return PositionOutSchema.model_validate(new_position).model_dump()

    @classmethod
    async def update_position_service(cls, auth: AuthSchema, data: PositionUpdateSchema) -> Dict:
        """更新岗位"""
        position = await PositionCRUD(auth).get_by_id_crud(id=data.id)
        if not position:
            raise CustomException(msg='更新失败，该岗位不存在')
        exist_position = await PositionCRUD(auth).get(name=data.name)
        if exist_position and exist_position.id != data.id:
            raise CustomException(msg='更新失败，岗位名称重复')
        updated_position = await PositionCRUD(auth).update(id=data.id, data=data)
        return PositionOutSchema.model_validate(updated_position).model_dump()

    @classmethod
    async def delete_position_service(cls, auth: AuthSchema, id: int) -> None:
        """删除岗位"""
        position = await PositionCRUD(auth).get_by_id_crud(id=id)
        if not position:
            raise CustomException(msg='删除失败，该岗位不存在')
        await PositionCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_position_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """设置岗位状态"""
        await PositionCRUD(auth).set_available_crud(ids=data.ids, available=data.available)

    @classmethod
    async def export_post_list_service(cls, post_list: List[Dict[str, Any]]) -> bytes:
        """导出岗位列表"""
        mapping_dict = {
            'id': '编号',
            'name': '岗位名称', 
            'order': '显示顺序',
            'available': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = post_list.copy()
        for item in data:
            item['available'] = '正常' if item.get('available') else '停用'

        return ExcelUtil.export_list2excel(list_data=post_list, mapping_dict=mapping_dict)