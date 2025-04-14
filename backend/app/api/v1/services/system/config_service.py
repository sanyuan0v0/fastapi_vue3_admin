# -*- coding: utf-8 -*-

import json
from typing import Dict

from aioredis import Redis
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from aioredis import Redis

from app.api.v1.schemas.system.auth_schema import AuthSchema
from app.api.v1.schemas.system.config_schema import ConfigOutSchema, ConfigUpdateSchema
from app.api.v1.cruds.system.config_crud import ConfigCRUD
from app.common.enums import RedisInitKeyConfig
from app.core.redis_crud import RedisCURD
from app.utils.upload_util import UploadUtil
from app.core.base_schema import UploadResponseSchema
from app.core.exceptions import CustomException
from app.config.setting import settings
from app.core.logger import logger


class ConfigService:
    """
    配置管理模块服务层
    """
    
    @classmethod
    async def get_service(cls, auth: AuthSchema, id: int) -> Dict:
        config_obj = await ConfigCRUD(auth).get_crud(id=id)
        return ConfigOutSchema.model_validate(config_obj).model_dump()

    @classmethod
    async def update_service(cls, auth: AuthSchema, redis: Redis, data: ConfigUpdateSchema) -> bool:
        new_obj = await ConfigCRUD(auth).update_crud(id=data.id, data=data)
        new_obj_dict = ConfigOutSchema.model_validate(new_obj).model_dump()
        
        # 保存到Redis并设置过期时间
        redis_key = f"{RedisInitKeyConfig.System_Config.key}:{'init_system_config'}"
        try:
            value = json.dumps(new_obj_dict, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                    expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            logger.info(f"更新系统配置成功: {new_obj_dict}")
            return True
        except Exception as e:
            logger.error(f"更新系统配置失败: {e}")
            raise CustomException(msg="更新系统配置失败")
        return new_obj_dict

    @classmethod
    async def upload_service(cls, base_url: str, file: UploadFile) -> Dict:
        """上传文件"""
        if not file:
            raise CustomException(msg="请选择要上传的文件")
        filename, filepath = await UploadUtil.upload_file(file=file)
        
        return UploadResponseSchema(
            file_path=f'{filepath}',
            file_name=filename,
            origin_name=file.filename,
            file_url=f'{base_url}{filepath}',
        ).model_dump()
    
    @classmethod
    async def init_config_service(cls, redis: Redis, db: AsyncSession)-> None:
        auth = AuthSchema(db=db)
        config_obj = await ConfigCRUD(auth).get_crud(id=1)
        config_obj_dict = ConfigOutSchema.model_validate(config_obj).model_dump()

        # 保存到Redis并设置过期时间
        redis_key = f"{RedisInitKeyConfig.System_Config.key}:{'init_system_config'}"
        try:
            value = json.dumps(config_obj_dict, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                    expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
        except Exception as e:
            logger.error(f"初始化系统配置失败: {e}")
            raise CustomException(msg="初始化系统配置失败")

    @classmethod
    async def get_init_config_service(cls, redis: Redis) -> Dict:
        """获取系统配置"""
        redis_key = f"{RedisInitKeyConfig.System_Config.key}:{'init_system_config'}"
        config_obj_list_dict = await RedisCURD(redis).get(redis_key)
        if not config_obj_list_dict:
            raise CustomException(msg="系统配置不存在")
        return json.loads(config_obj_list_dict)
    