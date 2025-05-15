# -*- coding: utf-8 -*-

from typing import Any, List, Dict

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.notice_schema import NoticeCreateSchema, NoticeUpdateSchema, NoticeOutSchema
from app.core.base_schema import BatchSetAvailable
from app.api.v1.params.system.notice_param import NoticeQueryParams
from app.api.v1.cruds.system.notice_crud import NoticeCRUD
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil


class NoticeService:
    """
    公告管理模块服务层
    """
    
    @classmethod
    async def get_notice_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        config_obj = await NoticeCRUD(auth).get_by_id_crud(id=id)
        return NoticeOutSchema.model_validate(config_obj).model_dump()
    
    @classmethod
    async def get_notice_list_service(cls, auth: AuthSchema, search: NoticeQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        if order_by:
            order_by = eval(order_by)
        config_obj_list = await NoticeCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [NoticeOutSchema.model_validate(config_obj).model_dump() for config_obj in config_obj_list]
    
    @classmethod
    async def create_notice_service(cls, auth: AuthSchema, data: NoticeCreateSchema) -> Dict:
        config = await NoticeCRUD(auth).get(notice_title=data.notice_title)
        if config:
            raise CustomException(msg='创建失败，该公告通知已存在')
        config_obj = await NoticeCRUD(auth).create_crud(data=data)
        return NoticeOutSchema.model_validate(config_obj).model_dump()
    
    @classmethod
    async def update_notice_service(cls, auth: AuthSchema, data: NoticeUpdateSchema) -> Dict:
        config = await NoticeCRUD(auth).get_by_id_crud(id=data.id)
        if not config:
            raise CustomException(msg='更新失败，该公告通知不存在')
        exist_config = await NoticeCRUD(auth).get(notice_title=data.notice_title)
        if exist_config and exist_config.id != data.id:
            raise CustomException(msg='更新失败，公告通知标题重复')
        config_obj = await NoticeCRUD(auth).update_crud(id=data.id, data=data)
        return NoticeOutSchema.model_validate(config_obj).model_dump()
    
    @classmethod
    async def delete_notice_service(cls, auth: AuthSchema, id: int) -> None:
        config = await NoticeCRUD(auth).get_by_id_crud(id=id)
        if not config:
            raise CustomException(msg='删除失败，该公告通知不存在')
        await NoticeCRUD(auth).delete_crud(ids=[id])
    
    @classmethod
    async def set_notice_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        await NoticeCRUD(auth).set_available_crud(ids=data.ids, available=data.available)
    
    @classmethod
    async def export_notice_service(cls, notice_list: List[Dict[str, Any]]) -> bytes:
        """导出公告列表"""
        mapping_dict = {
            'id': '编号',
            'notice_title': '公告标题', 
            'notice_type': '公告类型（1通知 2公告）',
            'notice_content': '公告内容',
            'available': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = notice_list.copy()
        for item in data:
            # 处理状态
            item['available'] = '正常' if item.get('available') else '停用'
            # 处理公告类型
            item['notice_type'] = '通知' if item.get('notice_type') == 1 else '公告'

        return ExcelUtil.export_list2excel(list_data=notice_list, mapping_dict=mapping_dict)