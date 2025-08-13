# -*- coding: utf-8 -*-

import json
from typing import Any, Dict, List, Union

from redis.asyncio.client import Redis
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from app.api.v1.params.system.config_param import ConfigQueryParams
from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.config_schema import ConfigOutSchema, ConfigUpdateSchema, ConfigCreateSchema, UpdataSystemConfigSchema
from app.api.v1.cruds.system.config_crud import ConfigCRUD
from app.common.enums import RedisInitKeyConfig
from app.core.redis_crud import RedisCURD
from app.utils.excel_util import ExcelUtil
from app.utils.upload_util import UploadUtil
from app.core.base_schema import UploadResponseSchema
from app.core.exceptions import CustomException
from app.core.logger import logger


class ConfigService:
    """
    配置管理模块服务层
    """
    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        obj = await ConfigCRUD(auth).get_obj_by_id_crud(id=id)
        return ConfigOutSchema.model_validate(obj).model_dump()
    

    @classmethod
    async def get_obj_list_service(cls, auth: AuthSchema, search: ConfigQueryParams = None, order_by: List[Dict[str, str]] = None) -> List[Dict]:
        if order_by:
            order_by = eval(order_by)
        obj_list = None
        if search:
            obj_list = await ConfigCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        else:
            obj_list = await ConfigCRUD(auth).get_obj_list_crud()
        return [ConfigOutSchema.model_validate(obj).model_dump() for obj in obj_list]
    
    @classmethod
    async def create_obj_service(cls, auth: AuthSchema, redis: Redis, data: ConfigCreateSchema) -> Dict:
        exist_obj = await ConfigCRUD(auth).get(config_key=data.config_key)
        if exist_obj:
            raise CustomException(msg='创建失败，该配置已存在')
        exist_obj = await ConfigCRUD(auth).get(config_key=data.config_key)
        if exist_obj:
            raise CustomException(msg='创建失败，该配置key已存在')
        obj = await ConfigCRUD(auth).create_obj_crud(data=data)

        new_obj_dict = ConfigOutSchema.model_validate(obj).model_dump()

        # 同步redis
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{data.config_key}"
        try:
            result = await RedisCURD(redis).set(
                key=redis_key,
                value="",
            )
            if not result:
                logger.error(f"同步配置到缓存失败: {new_obj_dict}")
                raise CustomException(msg="同步配置到缓存失败")
        except Exception as e:
            logger.error(f"创建字典类型失败: {e}")
            raise CustomException(msg=f"创建字典类型失败 {e}")
        
        return new_obj_dict
    
    @classmethod
    async def update_obj_service(cls, auth: AuthSchema, redis: Redis, data: ConfigUpdateSchema) -> Dict:
        exist_obj = await ConfigCRUD(auth).get_obj_by_id_crud(id=data.id)
        if not exist_obj:
            raise CustomException(msg='更新失败，该数系统配置不存在')
        if exist_obj.config_key != data.config_key:
            raise CustomException(msg='更新失败，系统配置key不允许修改')
        
        new_obj = await ConfigCRUD(auth).update_obj_crud(id=data.id, data=data)
        new_obj_dict = ConfigOutSchema.model_validate(new_obj).model_dump()

        # 同步redis
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{new_obj.config_key}"
        try:
            value = json.dumps(new_obj_dict, ensure_ascii=False)
            result = await RedisCURD(redis).set(
                key=redis_key,
                value=value,
            )
            if not result:
                logger.error(f"同步配置到缓存失败: {new_obj_dict}")
                raise CustomException(msg="同步配置到缓存失败")
        except Exception as e:
            logger.error(f"更新系统配置失败: {e}")
            raise CustomException(msg="更新系统配置失败")

        return new_obj_dict

    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, ids: list[int]) -> None:
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        for id in ids:
            exist_obj = await ConfigCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg='删除失败，该数据字典类型不存在')
            # 检查是否是否初始化类型
            if exist_obj.config_type:
                # 如果有字典数据，不能删除
                raise CustomException(msg=f'{exist_obj.config_name} 删除失败，系统初始化配置不可以删除')
        
        await ConfigCRUD(auth).delete_obj_crud(ids=ids)
        # 同步删除Redis缓存
        redis_key = f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{exist_obj.config_key}"
        try:
            await RedisCURD(redis).delete(redis_key)
            logger.info(f"删除系统配置成功: {id}")
        except Exception as e:
            logger.error(f"删除系统配置失败: {e}")
            raise CustomException(msg="删除字典类型失败")
    
    @classmethod
    async def export_obj_service(cls, data_list: List[Dict[str, Any]]) -> bytes:
        """导出系统配置列表"""
        mapping_dict = {
            'id': '编号',
            'config_name': '参数名称', 
            'config_key': '参数键名',
            'config_value': '参数键值',
            'config_type': '系统内置((True:是 False:否))',
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
            item['config_type'] = '是' if item.get('config_type') else '否'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data_list, mapping_dict=mapping_dict)
    
    @classmethod
    async def upload_service(cls, base_url: str, file: UploadFile) -> Dict:
        """上传文件"""
        if not file:
            raise CustomException(msg="请选择要上传的文件")
        filename, filepath, file_url = await UploadUtil.upload_file(file=file, base_url=base_url)
        
        return UploadResponseSchema(
            file_path=f'{filepath}',
            file_name=filename,
            origin_name=file.filename,
            file_url=f'{file_url}',
        ).model_dump()

    @classmethod
    async def init_config_service(cls, redis: Redis, db: AsyncSession) -> bool:
        auth = AuthSchema(db=db)
        config_obj = await ConfigCRUD(auth).get_obj_list_crud()
        if not config_obj:
            raise CustomException(msg="系统配置不存在")
        try:
            # 保存到Redis并设置过期时间
            for config in config_obj:
                redis_key = (f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:{config.config_key}")
                config_obj_dict = ConfigOutSchema.model_validate(config).model_dump()
                value = json.dumps(config_obj_dict, ensure_ascii=False)
                result = await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                )
                if not result:
                    logger.error(f"初始化系统配置失败: {config_obj_dict}")
                    raise CustomException(msg="初始化系统配置失败")
        except Exception as e:
            logger.error(f"初始化系统配置失败: {e}")
            raise CustomException(msg="初始化系统配置失败")

    @classmethod
    async def get_init_config_service(cls, redis: Redis) -> Dict:
        """获取系统配置"""
        redis_keys = await RedisCURD(redis).get_keys(f"{RedisInitKeyConfig.SYSTEM_CONFIG.key}:*")
        redis_configs = await RedisCURD(redis).mget(*redis_keys)
        configs = []
        for config in redis_configs:
            if not config:
                continue
            try:
                new_config = json.loads(config)  
                configs.append(new_config)
            except Exception as e:
                logger.error(f"解析系统配置数据失败: {e}")
                continue
        
        return configs
