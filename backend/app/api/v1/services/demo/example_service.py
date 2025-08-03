# -*- coding: utf-8 -*-

import io
from typing import Any, List, Dict
from fastapi import UploadFile
import pandas as pd

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.demo.example_schema import ExampleCreateSchema, ExampleUpdateSchema, ExampleOutSchema
from app.core.base_schema import BatchSetAvailable
from app.api.v1.params.demo.example_param import ExampleQueryParams
from app.api.v1.cruds.demo.example_crud import ExampleCRUD
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import logger


class ExampleService:
    """
    示例管理模块服务层
    """
    
    @classmethod
    async def get_example_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """详情"""
        obj = await ExampleCRUD(auth).get_by_id_crud(id=id)
        return ExampleOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_example_list_service(cls, auth: AuthSchema, search: ExampleQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        """列表查询"""
        if order_by:
            order_by = eval(order_by)
        obj_list = await ExampleCRUD(auth).get_list_crud(search=search.__dict__, order_by=order_by)
        return [ExampleOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_example_service(cls, auth: AuthSchema, data: ExampleCreateSchema) -> Dict:
        """创建"""
        obj = await ExampleCRUD(auth).get(name=data.name)
        if obj:
            raise CustomException(msg='创建失败，名称已存在')
        obj = await ExampleCRUD(auth).create_crud(data=data)
        return ExampleOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_example_service(cls, auth: AuthSchema, data: ExampleUpdateSchema) -> Dict:
        """更新"""
        obj = await ExampleCRUD(auth).get_by_id_crud(id=data.id)
        if not obj:
            raise CustomException(msg='更新失败，该数据不存在')
        exist_obj = await ExampleCRUD(auth).get(name=data.name)
        if exist_obj and exist_obj.id != data.id:
            raise CustomException(msg='更新失败，名称重复')
        obj = await ExampleCRUD(auth).update_crud(id=data.id, data=data)
        return ExampleOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_example_service(cls, auth: AuthSchema, ids: list[int]) -> None:
        """删除"""
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            obj = await ExampleCRUD(auth).get_by_id_crud(id=id)
            if not obj:
                raise CustomException(msg='删除失败，该数据不存在')
        await ExampleCRUD(auth).delete_crud(ids=ids)
    
    @classmethod
    async def set_example_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """批量设置状态"""
        await ExampleCRUD(auth).set_available_crud(ids=data.ids, status=data.status)
    
    @classmethod
    async def batch_export_service(cls, obj_list: List[Dict[str, Any]]) -> bytes:
        """批量导出"""
        mapping_dict = {
            'id': '编号',
            'name': '名称', 
            'status': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = obj_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '正常' if item.get('status') else '停用'
            # 处理公告类型
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=obj_list, mapping_dict=mapping_dict)

    @classmethod
    async def batch_import_service(cls, auth: AuthSchema, file: UploadFile, update_support: bool = False) -> str:
        """批量导入"""
        
        header_dict = {
            '名称': 'name',
            '状态': 'status',
            '描述': 'description'
        }

        try:
            # 读取Excel文件
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents))
            await file.close()
            
            if df.empty:
                raise CustomException(msg="导入文件为空")
            
            # 检查表头是否完整
            missing_headers = [header for header in header_dict.keys() if header not in df.columns]
            if missing_headers:
                raise CustomException(msg=f"导入文件缺少必要的列: {', '.join(missing_headers)}")
            
            # 重命名列名
            df.rename(columns=header_dict, inplace=True)
            
            # 验证必填字段
            required_fields = ['name', 'status']
            for field in required_fields:
                if df[field].isnull().any():
                    missing_rows = df[df[field].isnull()].index.tolist()
                    raise CustomException(msg=f"{[k for k,v in header_dict.items() if v == field][0]}不能为空，第{[i+1 for i in missing_rows]}行")
            
            error_msgs = []
            success_count = 0
            
            # 处理每一行数据
            for index, row in df.iterrows():
                try:
                    # 数据转换前的类型检查
                    try:
                        name = str(row['name'])
                    except ValueError:
                        error_msgs.append(f"第{index+1}行: 名称必须是字符串")
                        continue
                    try:
                        status = True if row['status'] == '正常' else False
                    except ValueError:
                        error_msgs.append(f"第{index+1}行: 状态必须是'正常'或'停用'")
                        continue
                    
                    # 构建用户数据
                    data = {
                        "name": name,
                        "status": status,
                        "description": str(row['description']).strip() if not pd.isna(row['description']) else None,
                    }

                    # 处理用户导入
                    exists_user = await ExampleCRUD(auth).get(name=data["name"])
                    if exists_user:
                        if update_support:
                            await ExampleCRUD(auth).update(id=exists_user.id, data=data)
                            success_count += 1
                        else:
                            error_msgs.append(f"第{index+1}行: 用户 {data['username']} 已存在")
                    else:
                        await ExampleCRUD(auth).create(data=data)
                        success_count += 1
                        
                except Exception as e:
                    error_msgs.append(f"第{index+1}行: {str(e)}")
                    continue

            # 返回详细的导入结果
            result = f"成功导入 {success_count} 条数据"
            if error_msgs:
                result += "\n错误信息:\n" + "\n".join(error_msgs)
            return result
            
        except Exception as e:
            logger.error(f"批量导入用户失败: {str(e)}")
            raise CustomException(msg=f"导入失败: {str(e)}")

    @classmethod
    async def import_template_download_service(cls) -> bytes:
        """下载导入模板"""
        header_list = ['名称', '状态', '描述']
        selector_header_list = ['状态'] 
        option_list = [{'状态': ['正常', '停用']}]
        return ExcelUtil.get_excel_template(
            header_list=header_list,
            selector_header_list=selector_header_list,
            option_list=option_list
        )