# -*- coding: utf-8 -*-

import json
from typing import Any, List, Dict
from aioredis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.dict_schema import DictDataCreateSchema,DictDataOutSchema,DictDataUpdateSchema,DictTypeCreateSchema,DictTypeOutSchema,DictTypeUpdateSchema
from app.common.enums import RedisInitKeyConfig
from app.api.v1.params.system.dict_param import DictDataQueryParams, DictTypeQueryParams
from app.api.v1.cruds.system.dict_crud import DictDataCRUD, DictTypeCRUD
from app.core.redis_crud import RedisCURD
from app.core.exceptions import CustomException
from app.utils.excel_util import ExcelUtil
from app.core.logger import logger
from app.config.setting import settings

class DictTypeService:
    """
    字典类型管理模块服务层
    """
    
    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await DictTypeCRUD(auth).get_obj_by_id_crud(id=id)
        return DictTypeOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_obj_list_service(cls, auth: AuthSchema, search: DictTypeQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        if order_by:
            order_by = eval(order_by)
        if search:
            obj_list = await DictTypeCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        obj_list = await DictTypeCRUD(auth).get_obj_list_crud()
        return [DictTypeOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictTypeCreateSchema) -> Dict:
        exist_obj = await DictTypeCRUD(auth).get(dict_name=data.dict_name)
        if exist_obj:
            raise CustomException(msg='创建失败，该数据字典类型已存在')
        obj = await DictTypeCRUD(auth).create_obj_crud(data=data)

        new_obj_dict = DictTypeOutSchema.model_validate(obj).model_dump()
        
        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{data.dict_type}"
        
        try:
            await RedisCURD(redis).set(
                    key=redis_key,
                    value="",
                    expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            logger.info(f"创建字典类型成功: {new_obj_dict}")
        except Exception as e:
            logger.error(f"创建字典类型失败: {e}")
            raise CustomException(msg=f"创建字典类型失败 {e}")
        
        return new_obj_dict
    
    @classmethod
    async def update_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictTypeUpdateSchema) -> Dict:
        exist_obj = await DictTypeCRUD(auth).get_obj_by_id_crud(id=data.id)
        if not exist_obj:
            raise CustomException(msg='更新失败，该数据字典类型不存在')
        if exist_obj.dict_name != data.dict_name:
            raise CustomException(msg='更新失败，数据字典类型名称不可以修改')
        
        
        dict_data_list = []
        # 如果字典类型修改或状态变更，则修改对应字典数据的类型和状态，并更新Redis缓存
        if exist_obj.dict_type != data.dict_type or exist_obj.available != data.available:
            # 检查字典数据类型是否被修改
            exist_obj_type_list = await DictDataCRUD(auth).list(search={'dict_type': exist_obj.dict_type})
            if exist_obj_type_list:
                for item in exist_obj_type_list:
                    item.dict_type = data.dict_type
                    dict_data = DictDataUpdateSchema(
                        id=item.id,
                        dict_sort=item.dict_sort,
                        dict_label=item.dict_label,
                        dict_value=item.dict_value,
                        dict_type=data.dict_type,
                        css_class=item.css_class,
                        list_class=item.list_class,
                        is_default=item.is_default,
                        available=data.available,
                        description=item.description
                    )
                    obj = await DictDataCRUD(auth).update_obj_crud(id=item.id, data=dict_data)
                    dict_data_list.append(DictDataOutSchema.model_validate(obj).model_dump())
        
        obj = await DictTypeCRUD(auth).update_obj_crud(id=data.id, data=data)

        new_obj_dict = DictTypeOutSchema.model_validate(obj).model_dump()

        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据，确保包含最新状态
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                    expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            logger.info(f"更新字典类型成功并刷新缓存: {new_obj_dict}")
        except Exception as e:
            logger.error(f"更新字典类型缓存失败: {e}")
            raise CustomException(msg=f"更新字典类型缓存失败 {e}")
        
        return new_obj_dict
    
    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, id: int) -> None:
        exist_obj = await DictTypeCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg='删除失败，该数据字典类型不存在')
        # 检查是否有字典数据
        exist_obj_type_list = await DictDataCRUD(auth).list(search={'dict_type': id})
        if len(exist_obj_type_list) > 0:
            # 如果有字典数据，不能删除
            raise CustomException(msg='删除失败，该数据字典类型下存在字典数据')
        await DictTypeCRUD(auth).delete_obj_crud(ids=[id])
        # 删除Redis缓存
        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{exist_obj.dict_type}"
        try:
            await RedisCURD(redis).delete(redis_key)
            logger.info(f"删除字典类型成功: {id}")
        except Exception as e:
            logger.error(f"删除字典类型失败: {e}")
            raise CustomException(msg=f"删除字典类型失败 {e}")

    @classmethod
    async def export_obj_service(cls, data_list: List[Dict[str, Any]]) -> bytes:
        """导出公告列表"""
        mapping_dict = {
            'id': '编号',
            'dict_name': '字典名称', 
            'dict_type': '字典类型',
            'available': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            # 处理状态
            item['available'] = '正常' if item.get('available') else '停用'

        return ExcelUtil.export_list2excel(list_data=data_list, mapping_dict=mapping_dict)
    

class DictDataService:
    """
    字典数据管理模块服务层
    """
    
    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_obj_list_service(cls, auth: AuthSchema, search: DictDataQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        if order_by:
            order_by = eval(order_by)
        obj_list = await DictDataCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        return [DictDataOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def init_dict_service(cls, redis: Redis, db: AsyncSession):
        """应用初始化: 获取所有字典类型对应的字典数据信息并缓存service"""

        auth = AuthSchema(db=db)
        obj_list = await DictTypeCRUD(auth).get_obj_list_crud()
        if not obj_list:
            logger.warning("未找到任何字典类型数据")
            return
        for obj in obj_list:
            dict_type = obj.dict_type
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': dict_type})
            
            if not dict_data_list:
                logger.warning(f"字典类型 {dict_type} 未找到对应的字典数据")
                continue
            
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
    
            # 保存到Redis并设置过期时间
            redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{dict_type}"
            try:
                value = json.dumps(dict_data, ensure_ascii=False)
                await RedisCURD(redis).set(
                        key=redis_key,
                        value=value,
                        expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                    )
            except Exception as e:
                logger.error(f"初始化字典数据失败: {e}")
                raise CustomException(msg=f"初始化字典数据成功 {e}")
    
    @classmethod
    async def get_init_dict_service(cls, redis: Redis) -> Dict:
        """获取系统配置"""
        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:*"
        obj_list_dict = await RedisCURD(redis).get_keys(redis_key)
        cache_key_list = [key.split(':', 1)[1] for key in obj_list_dict if key.startswith(f'{RedisInitKeyConfig.System_Dict.key}:')]
        logger.info(f"获取字典数据：{cache_key_list}")
        if not cache_key_list:
            raise CustomException(msg="字典数据不存在")
        return cache_key_list
    
    @classmethod
    async def query_init_dict_service(cls, redis: Redis, dict_type: str):
        """从缓存获取字典数据列表信息service"""
        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{dict_type}"
        obj_list_dict = await RedisCURD(redis).get(redis_key)
        if not obj_list_dict:
            raise CustomException(msg="数据字典不存在")
        return obj_list_dict

    @classmethod
    async def create_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictDataCreateSchema) -> Dict:
        exist_obj = await DictDataCRUD(auth).get(dict_label=data.dict_label)
        if exist_obj:
            raise CustomException(msg='创建失败，该字典数据已存在')
        obj = await DictDataCRUD(auth).create_obj_crud(data=data)

        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                    expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            logger.info(f"创建字典数据写入缓存成功: {obj}")
        except Exception as e:
            logger.error(f"创建字典数据写入缓存失败: {e}")
            raise CustomException(msg=f"创建字典数据失败 {e}")

        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictDataUpdateSchema) -> Dict:
        exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=data.id)
        if not exist_obj:
            raise CustomException(msg='更新失败，该字典数据不存在')
        exist_obj = await DictDataCRUD(auth).get(dict_label=data.dict_label)
        if exist_obj and exist_obj.id != data.id:
            raise CustomException(msg='更新失败，数据字典数据重复')
            
        # 如果状态变更，需要同步更新字典类型状态并刷新缓存
        if exist_obj.available != data.available:
            dict_type = await DictTypeCRUD(auth).get(dict_type=exist_obj.dict_type)
            if dict_type:
                update_data = DictTypeUpdateSchema(
                    id=dict_type.id,
                    dict_name=dict_type.dict_name,
                    dict_type=dict_type.dict_type,
                    available=data.available,
                    description=dict_type.description
                )
                await DictTypeCRUD(auth).update_obj_crud(id=dict_type.id, data=update_data)
                # 刷新Redis缓存
                redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{dict_type.dict_type}"
                try:
                    dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': dict_type.dict_type})
                    dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
                    value = json.dumps(dict_data, ensure_ascii=False)
                    await RedisCURD(redis).set(
                            key=redis_key,
                            value=value,
                            expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                        )
                except Exception as e:
                    logger.error(f"更新字典数据状态时刷新缓存失败: {e}")
                
        obj = await DictDataCRUD(auth).update_obj_crud(id=data.id, data=data)
        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                    expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            logger.info(f"更新字典数据写入缓存成功: {obj}")
        except Exception as e:
            logger.error(f"更新字典数据写入缓存失败: {e}")
            raise CustomException(msg=f"更新字典数据失败 {e}")

        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, id: int) -> None:
        exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg='删除失败，该字典数据不存在')
        await DictDataCRUD(auth).delete_obj_crud(ids=[id])
        # 删除Redis缓存
        redis_key = f"{RedisInitKeyConfig.System_Dict.key}:{exist_obj.dict_type}"
        try:
            # 删除Redis缓存
            await RedisCURD(redis).delete(redis_key)
            logger.info(f"删除字典数据成功: {id}")
        except Exception as e:
            logger.error(f"删除字典数据失败: {e}")
            raise CustomException(msg=f"删除字典数据失败 {e}")

    @classmethod
    async def export_obj_service(cls, data_list: List[Dict[str, Any]]) -> bytes:
        """导出公告列表"""
        mapping_dict = {
            'id': '编号',
            'dict_sort': '字典排序', 
            'dict_label': '字典标签', 
            'dict_value': '字典键值', 
            'dict_type': '字典类型',
            'css_class': '样式属性', 
            'list_class': '表格回显样式', 
            'is_default': '是否默认', 
            'available': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            # 处理状态
            item['available'] = '正常' if item.get('available') else '停用'
            # 处理是否默认
            item['is_default'] = '是' if item.get('is_default') else '否'

        return ExcelUtil.export_list2excel(list_data=data_list, mapping_dict=mapping_dict)