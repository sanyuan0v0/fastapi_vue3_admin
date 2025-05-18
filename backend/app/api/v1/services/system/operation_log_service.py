# -*- coding: utf-8 -*-

from typing import Any, Dict, List


from app.api.v1.cruds.system.operation_log_crud import OperationLogCRUD
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.operation_log_schema import (
    OperationLogCreateSchema,
    OperationLogOutSchema
)
from app.utils.excel_util import ExcelUtil
from app.api.v1.params.system.operation_log_param import OperationLogQueryParams


class OperationLogService:
    """
    日志模块服务层
    """

    @classmethod
    async def get_log_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """获取日志详情"""
        log = await OperationLogCRUD(auth).get_by_id_crud(id=id)
        log_dict = OperationLogOutSchema.model_validate(log).model_dump()
        return log_dict

    @classmethod
    async def get_log_list_service(cls, auth: AuthSchema, search: OperationLogQueryParams, order_by: List[Dict] = None) -> List[Dict]:
        """获取日志列表"""
        if order_by:
            order_by = eval(order_by)
        else:
            order_by = [{"created_at": "desc"}]
        log_list = await OperationLogCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        log_dict_list = [OperationLogOutSchema.model_validate(log).model_dump() for log in log_list]
        return log_dict_list

    @classmethod
    async def create_log_service(cls, auth: AuthSchema, data: OperationLogCreateSchema) -> Dict:
        """创建日志"""
        new_log = await OperationLogCRUD(auth).create(data=data)
        new_log_dict = OperationLogOutSchema.model_validate(new_log).model_dump()
        return new_log_dict
    
    @classmethod
    async def delete_log_service(cls, auth: AuthSchema, id: int) -> None:
        """删除日志"""
        await OperationLogCRUD(auth).delete(ids=[id])

    @classmethod
    async def export_log_list_service(cls, operation_log_list: List[Dict[str, Any]]) -> bytes:
        """
        导出日志信息

        Args:
            operation_log_list: 操作日志信息列表
        
        Returns:
            bytes: 操作日志信息excel的二进制数据
        """
        # 操作日志字段映射
        mapping_dict = {
            'id': '编号',
            'request_path': '请求URL',
            'request_method': '请求方式',
            'request_payload': '请求参数',
            'request_ip': '操作地址',
            'login_location': '登录位置',
            'request_os': '操作系统',
            'request_browser': '浏览器',
            'response_json': '返回参数',
            'response_code': '相应状态',
            'process_time': '处理时间',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 处理数据
        data = operation_log_list.copy()
        for item in data:
            # 处理状态
            item['response_code'] = '成功' if item.get('response_code') == 200 else '失败'

        return ExcelUtil.export_list2excel(list_data=operation_log_list, mapping_dict=mapping_dict)
